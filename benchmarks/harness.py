from __future__ import annotations

from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import threading
import time
import traceback
from typing import Any, Callable

import numba
import numpy as np
import psutil
import torch


CATEGORY_ORDER = [
    "single_threaded",
    "parallel",
    "memory_bound",
    "compute_bound",
]

THREAD_ENV_KEYS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "NPY_NUM_THREADS",
)


def _command_output(cmd: list[str]) -> str | None:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except Exception:
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def _parse_key_value_block(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip()
    return None


def _linux_cpu_model() -> str | None:
    lscpu = _command_output(["lscpu"])
    if lscpu:
        for key in ("Model name", "Architecture"):
            value = _parse_key_value_block(lscpu, key)
            if value and value.lower() not in {"x86_64", "amd64", "aarch64", "arm64"}:
                return value

    cpuinfo = Path("/proc/cpuinfo")
    try:
        for line in cpuinfo.read_text(encoding="utf-8").splitlines():
            if ":" not in line:
                continue
            key, value = (part.strip() for part in line.split(":", 1))
            if key in {"model name", "Hardware", "Processor"} and value:
                if value.lower() not in {"x86_64", "amd64", "aarch64", "arm64"}:
                    return value
    except OSError:
        pass

    return None


def _linux_model_name() -> str | None:
    candidates = (
        Path("/sys/devices/virtual/dmi/id/product_name"),
        Path("/sys/devices/virtual/dmi/id/board_name"),
    )
    for path in candidates:
        try:
            value = path.read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if value and value.lower() not in {"default string", "to be filled by o.e.m."}:
            return value
    return None


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "machine"


def machine_label_from_system_info(system_info: dict[str, Any]) -> str:
    if system_info.get("machine_name"):
        return str(system_info["machine_name"])

    chip = system_info.get("chip") or system_info.get("processor")
    model = system_info.get("model_name")
    details: list[str] = []
    if chip:
        details.append(str(chip))
    if model and str(model) not in details:
        details.append(str(model))
    if details:
        return " / ".join(details)
    if system_info.get("system") and system_info.get("machine"):
        return f"{system_info['system']} / {system_info['machine']}"
    return str(system_info.get("machine") or system_info.get("system") or "unknown")


def machine_slug_from_system_info(system_info: dict[str, Any]) -> str:
    if system_info.get("machine_slug"):
        return str(system_info["machine_slug"])
    return _slugify(machine_label_from_system_info(system_info))


def sanitize_system_info(system_info: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {
        "generated_at": system_info.get("generated_at"),
        "system": system_info.get("system"),
        "machine": system_info.get("machine"),
        "python": system_info.get("python"),
        "processor": system_info.get("processor"),
        "logical_cores": system_info.get("logical_cores"),
        "physical_cores": system_info.get("physical_cores"),
        "memory_total_bytes": system_info.get("memory_total_bytes"),
        "memory_available_bytes": system_info.get("memory_available_bytes"),
        "torch_version": system_info.get("torch_version"),
        "numba_threads": system_info.get("numba_threads"),
    }

    for key in ("cpu_freq_mhz", "cpu_freq_max_mhz", "model_name", "chip",
                 "blas_backend", "blas_version", "lapack_backend", "lapack_version"):
        if system_info.get(key) is not None:
            sanitized[key] = system_info[key]

    sanitized["machine_name"] = machine_label_from_system_info(system_info)
    sanitized["machine_slug"] = machine_slug_from_system_info(sanitized)
    return sanitize_json({k: v for k, v in sanitized.items() if v is not None})


def get_system_info() -> dict[str, Any]:
    mem = psutil.virtual_memory()
    info: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "system": platform.system(),
        "machine": platform.machine() or "N/A",
        "python": platform.python_version(),
        "processor": platform.processor() or "N/A",
        "logical_cores": psutil.cpu_count(logical=True) or os.cpu_count(),
        "physical_cores": psutil.cpu_count(logical=False),
        "memory_total_bytes": int(mem.total),
        "memory_available_bytes": int(mem.available),
        "torch_version": torch.__version__,
        "numba_threads": numba.get_num_threads(),
    }

    freq = psutil.cpu_freq()
    if freq is not None:
        info["cpu_freq_mhz"] = float(freq.current)
        info["cpu_freq_max_mhz"] = float(freq.max)

    try:
        np_config = np.show_config(mode="dicts")
        deps = np_config.get("Build Dependencies", {})
        for lib in ("blas", "lapack"):
            lib_info = deps.get(lib, {})
            if lib_info:
                info[f"{lib}_backend"] = lib_info.get("name") or lib_info.get("detection method", "unknown")
                if lib_info.get("version"):
                    info[f"{lib}_version"] = lib_info["version"]
    except Exception:
        pass

    if platform.system() == "Darwin":
        processor = _command_output(["sysctl", "-n", "machdep.cpu.brand_string"])
        hw_info = _command_output(["system_profiler", "SPHardwareDataType"])
        if processor:
            info["processor"] = processor
        if hw_info:
            for key in ("Model Name", "Chip", "Processor Name"):
                value = _parse_key_value_block(hw_info, key)
                if value:
                    info[key.lower().replace(" ", "_")] = value
    elif platform.system() == "Linux":
        processor = _linux_cpu_model()
        model_name = _linux_model_name()
        if processor:
            info["processor"] = processor
        if model_name:
            info["model_name"] = model_name

    return sanitize_system_info(info)


def print_system_info(info: dict[str, Any]) -> None:
    print("=" * 72)
    print("SYSTEM INFORMATION")
    print("=" * 72)
    print(f"  Machine      : {machine_label_from_system_info(info)}")
    print(f"  System       : {info['system']}")
    print(f"  Architecture : {info['machine']}")
    print(f"  Processor    : {info['processor']}")
    if info.get("chip"):
        print(f"  Chip         : {info['chip']}")
    if info.get("model_name"):
        print(f"  Model Name   : {info['model_name']}")
    print(
        f"  CPU Cores    : {info['logical_cores']} logical / "
        f"{info['physical_cores']} physical"
    )
    if info.get("cpu_freq_mhz") is not None:
        print(
            f"  CPU Freq     : {info['cpu_freq_mhz']:.0f} MHz "
            f"(max {info.get('cpu_freq_max_mhz', 0.0):.0f} MHz)"
        )
    print(f"  Python       : {info['python']}")
    print(f"  Torch        : {info['torch_version']}")
    print(f"  RAM Total    : {info['memory_total_bytes'] / 1e9:.1f} GB")
    print(f"  RAM Free     : {info['memory_available_bytes'] / 1e9:.1f} GB")
    if info.get("blas_backend"):
        blas = info["blas_backend"]
        if info.get("blas_version"):
            blas += f" {info['blas_version']}"
        print(f"  BLAS         : {blas}")
    print("=" * 72)
    print()


class ResourceMonitor:
    """Sample process RSS memory and process CPU% in the background."""

    def __init__(self, interval: float = 0.05):
        self.interval = interval
        self._proc = psutil.Process()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.cpu_samples: list[float] = []
        self.mem_samples: list[int] = []

    def start(self) -> None:
        self.cpu_samples.clear()
        self.mem_samples.clear()
        self._stop.clear()
        self._proc.cpu_percent(interval=None)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join()

    def _run(self) -> None:
        while not self._stop.is_set():
            self.mem_samples.append(self._proc.memory_info().rss)
            self.cpu_samples.append(self._proc.cpu_percent(interval=self.interval))

    @property
    def peak_mem_gb(self) -> float:
        return max(self.mem_samples, default=0) / 1e9

    @property
    def avg_mem_gb(self) -> float:
        return float(np.mean(self.mem_samples)) / 1e9 if self.mem_samples else 0.0

    @property
    def avg_cpu_pct(self) -> float:
        return float(np.mean(self.cpu_samples)) if self.cpu_samples else 0.0

    @property
    def peak_cpu_pct(self) -> float:
        return max(self.cpu_samples, default=0.0)


@dataclass
class BenchmarkSpec:
    category: str
    name: str
    description: str
    runner: Callable[[], Any]
    threads: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    warmup: Callable[[], Any] | None = None
    setup: Callable[[], Any] | None = None
    teardown: Callable[[], Any] | None = None


@dataclass
class BenchmarkResult:
    category: str
    name: str
    description: str
    status: str
    threads: int | None
    wall_time_sec: float
    peak_mem_gb: float
    avg_mem_gb: float
    avg_cpu_pct: float
    peak_cpu_pct: float
    avg_cores_used: float
    peak_cores_used: float
    result: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return sanitize_json(asdict(self))


def sanitize_json(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): sanitize_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize_json(item) for item in value]
    if isinstance(value, np.ndarray):
        if value.ndim == 0:
            return sanitize_json(value.item())
        if np.issubdtype(value.dtype, np.number):
            return {
                "shape": list(value.shape),
                "dtype": str(value.dtype),
                "mean": float(np.mean(value)),
                "std": float(np.std(value)),
                "min": float(np.min(value)),
                "max": float(np.max(value)),
            }
        return {"shape": list(value.shape), "dtype": str(value.dtype)}
    return repr(value)


def summarize_payload(payload: Any) -> dict[str, Any] | None:
    if payload is None:
        return None
    if isinstance(payload, dict):
        return sanitize_json(payload)
    if isinstance(payload, (int, float, str, bool, np.generic)):
        return {"value": sanitize_json(payload)}
    if isinstance(payload, np.ndarray):
        return sanitize_json(payload)
    return {"value": sanitize_json(payload)}


@contextmanager
def controlled_threads(thread_count: int | None):
    if thread_count is None:
        yield
        return

    thread_count = max(1, int(thread_count))
    previous_env = {key: os.environ.get(key) for key in THREAD_ENV_KEYS}
    previous_numba = numba.get_num_threads()
    previous_torch = torch.get_num_threads()

    for key in THREAD_ENV_KEYS:
        os.environ[key] = str(thread_count)

    numba.set_num_threads(min(thread_count, numba.config.NUMBA_NUM_THREADS))
    torch.set_num_threads(thread_count)

    try:
        yield
    finally:
        for key, value in previous_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        numba.set_num_threads(previous_numba)
        torch.set_num_threads(previous_torch)


def run_benchmark(spec: BenchmarkSpec) -> BenchmarkResult:
    print("=" * 72)
    print(f"{spec.category.upper()} :: {spec.name}")
    print("=" * 72)
    print(spec.description)
    if spec.threads is None:
        print("  Threads     : default / all available")
    else:
        print(f"  Threads     : {spec.threads}")
    if spec.metadata:
        for key, value in spec.metadata.items():
            print(f"  {key:<11}: {value}")

    monitor = ResourceMonitor(interval=0.05)
    payload: Any = None
    error: str | None = None
    status = "ok"
    logical_cores = float(psutil.cpu_count(logical=True) or os.cpu_count() or 1)
    wall_time_sec = 0.0
    monitor_started = False
    t0 = 0.0

    with controlled_threads(spec.threads):
        try:
            if spec.warmup is not None:
                spec.warmup()
            if spec.setup is not None:
                spec.setup()
            monitor.start()
            monitor_started = True
            t0 = time.perf_counter()
            payload = spec.runner()
        except Exception as exc:
            status = "failed"
            error = f"{type(exc).__name__}: {exc}"
            traceback.print_exc()
        finally:
            if monitor_started:
                wall_time_sec = time.perf_counter() - t0
                monitor.stop()
            if spec.teardown is not None:
                try:
                    spec.teardown()
                except Exception as exc:
                    if status == "ok":
                        status = "failed"
                        error = f"{type(exc).__name__}: {exc}"
                    traceback.print_exc()

    result = BenchmarkResult(
        category=spec.category,
        name=spec.name,
        description=spec.description,
        status=status,
        threads=spec.threads,
        wall_time_sec=wall_time_sec,
        peak_mem_gb=monitor.peak_mem_gb,
        avg_mem_gb=monitor.avg_mem_gb,
        avg_cpu_pct=monitor.avg_cpu_pct,
        peak_cpu_pct=monitor.peak_cpu_pct,
        avg_cores_used=monitor.avg_cpu_pct / 100.0,
        peak_cores_used=monitor.peak_cpu_pct / 100.0,
        result=summarize_payload(payload),
        metadata=sanitize_json(spec.metadata),
        error=error,
    )

    print(f"  Status      : {result.status}")
    print(f"  Wall Time   : {result.wall_time_sec:.3f} s")
    print(f"  Peak Mem    : {result.peak_mem_gb:.3f} GB")
    print(f"  Avg Mem     : {result.avg_mem_gb:.3f} GB")
    print(f"  Avg CPU     : {result.avg_cpu_pct:.1f}%")
    print(f"  Peak CPU    : {result.peak_cpu_pct:.1f}%")
    print(
        f"  Avg Cores   : {result.avg_cores_used:.2f} / {logical_cores:.0f}"
    )
    print(
        f"  Peak Cores  : {result.peak_cores_used:.2f} / {logical_cores:.0f}"
    )
    if result.error:
        print(f"  Error       : {result.error}")
    elif result.result:
        for key, value in result.result.items():
            if isinstance(value, dict):
                continue
            print(f"  {key:<11}: {value}")
    print()

    return result


def save_results(
    results: list[BenchmarkResult],
    path: str | Path,
    *,
    system_info: dict[str, Any],
    run_metadata: dict[str, Any],
) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 2,
        "system_info": sanitize_system_info(system_info),
        "run_metadata": sanitize_json(run_metadata),
        "results": [result.to_dict() for result in results],
    }
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return destination


def load_results(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def default_results_path(
    output_dir: str | Path, profile: str, system_info: dict[str, Any]
) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    machine_slug = machine_slug_from_system_info(system_info)
    return Path(output_dir) / f"{machine_slug}_{profile}_{timestamp}.json"


def compute_scores(results: list[BenchmarkResult]) -> dict[str, float]:
    """Compute per-benchmark, per-category, and overall scores.

    Score = 1000 / wall_time_sec.  Higher = faster.
    Category score = geometric mean of its benchmark scores.
    Overall score = geometric mean of the four category scores.
    """
    from collections import defaultdict

    scores: dict[str, float] = {}
    category_scores: dict[str, list[float]] = defaultdict(list)

    for r in results:
        if r.status != "ok" or r.wall_time_sec <= 0:
            continue
        s = 1000.0 / r.wall_time_sec
        scores[r.name] = s
        category_scores[r.category].append(s)

    for cat, cat_scores in category_scores.items():
        if cat_scores:
            scores[f"_category_{cat}"] = float(
                np.exp(np.mean(np.log(cat_scores)))
            )

    cat_vals = [v for k, v in scores.items() if k.startswith("_category_")]
    if cat_vals:
        scores["_overall"] = float(np.exp(np.mean(np.log(cat_vals))))

    return scores


def print_summary_table(results: list[BenchmarkResult]) -> None:
    if not results:
        return

    scores = compute_scores(results)

    print("=" * 72)
    print("SCORE SUMMARY")
    print("=" * 72)
    overall = scores.get("_overall", 0.0)
    print(f"  Overall Score : {overall:,.0f}")
    for cat in CATEGORY_ORDER:
        cat_score = scores.get(f"_category_{cat}", 0.0)
        print(f"  {cat.replace('_', ' ').title():<18}: {cat_score:,.0f}")
    print()

    print("=" * 72)
    print("DETAILED RESULTS")
    print("=" * 72)
    header = f"{'Category':<18} {'Benchmark':<28} {'Status':<8} {'Time (s)':>10} {'Score':>10}"
    print(header)
    print("-" * len(header))
    for result in results:
        s = scores.get(result.name, 0.0)
        print(
            f"{result.category:<18} "
            f"{result.name[:28]:<28} "
            f"{result.status:<8} "
            f"{result.wall_time_sec:>10.3f}"
            f"{s:>10.0f}"
        )
    print()


def print_measurement_assessment(
    results: list[BenchmarkResult],
    *,
    logical_cores: int,
    profile: str,
) -> None:
    if not results:
        return

    min_runtime_by_profile = {
        "quick": 0.10,
        "default": 0.20,
        "full": 0.20,
        "fixed": 0.20,
    }
    min_runtime = min_runtime_by_profile.get(profile, 0.10)

    too_short = [
        result for result in results
        if result.status == "ok" and result.wall_time_sec < min_runtime
    ]
    single_thread_leaks = [
        result for result in results
        if result.status == "ok"
        and result.category == "single_threaded"
        and result.peak_cores_used > 1.25
    ]

    multi_threaded = [
        result for result in results
        if result.status == "ok" and result.threads is None
    ]
    all_core = [
        result for result in multi_threaded
        if result.avg_cores_used >= 0.75 * logical_cores
    ]
    partial_core = [
        result for result in multi_threaded
        if 1.5 <= result.avg_cores_used < 0.75 * logical_cores
    ]
    print("=" * 72)
    print("MEASUREMENT ASSESSMENT")
    print("=" * 72)
    print(f"  Quick/Min Runtime Threshold : {min_runtime:.2f} s")
    print(f"  Logical Cores              : {logical_cores}")

    if too_short:
        print("  Too Short:")
        for result in too_short:
            print(f"    - {result.category}/{result.name}: {result.wall_time_sec:.3f} s")
    else:
        print("  Too Short: none")

    if single_thread_leaks:
        print("  Single-Thread Leakage:")
        for result in single_thread_leaks:
            print(
                f"    - {result.name}: peak {result.peak_cores_used:.2f} cores"
            )
    else:
        print("  Single-Thread Leakage: none")

    if all_core:
        print("  All-Core Saturation:")
        for result in all_core:
            print(
                f"    - {result.category}/{result.name}: "
                f"avg {result.avg_cores_used:.2f}, peak {result.peak_cores_used:.2f}"
            )
    else:
        print("  All-Core Saturation: none")

    if partial_core:
        print("  Partial Multi-Core:")
        for result in partial_core:
            print(
                f"    - {result.category}/{result.name}: "
                f"avg {result.avg_cores_used:.2f}, peak {result.peak_cores_used:.2f}"
            )
    print()
