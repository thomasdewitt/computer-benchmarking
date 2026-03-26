from __future__ import annotations

import numpy as np

from .harness import BenchmarkSpec


WRITE_BYTES = 2_571_053_986
COPY_BYTES = 1_414_079_692
TRANSPOSE_BYTES = 1_414_079_692
SORT_BYTES = 942_719_795
MASK_BYTES = 1_131_263_754


def get_benchmarks(system_info: dict | None = None) -> list[BenchmarkSpec]:
    del system_info
    itemsize = np.dtype(np.float32).itemsize
    write_bytes = WRITE_BYTES
    copy_bytes = COPY_BYTES
    transpose_bytes = TRANSPOSE_BYTES
    sort_bytes = SORT_BYTES
    mask_bytes = MASK_BYTES

    write_count = write_bytes // itemsize
    copy_count = copy_bytes // itemsize
    sort_count = sort_bytes // itemsize
    mask_count = mask_bytes // itemsize

    write_state: dict[str, np.ndarray] = {}
    copy_state: dict[str, np.ndarray] = {}
    transpose_state: dict[str, np.ndarray] = {}
    sort_state: dict[str, np.ndarray] = {}
    mask_state: dict[str, np.ndarray] = {}

    def setup_write() -> None:
        write_state["base"] = np.empty(write_count, dtype=np.float32)

    def setup_copy() -> None:
        copy_state["base"] = np.random.default_rng(21).standard_normal(copy_count).astype(np.float32)

    def setup_transpose() -> None:
        edge = max(
            64,
            int(round((transpose_bytes / itemsize) ** (1.0 / 3.0))),
        )
        transpose_state["cube"] = np.random.default_rng(22).standard_normal(
            (edge, edge, edge // 2),
        ).astype(np.float32)

    def setup_sort() -> None:
        sort_state["values"] = np.random.default_rng(23).standard_normal(sort_count).astype(np.float32)

    def setup_mask() -> None:
        values = np.random.default_rng(24).standard_normal(mask_count).astype(np.float32)
        mask = values > np.float32(0.0)
        mask_state["values"] = values
        mask_state["mask"] = mask

    def run_write():
        write_state["base"].fill(np.float32(1.0))
        return {
            "bytes_written": int(write_state["base"].nbytes),
            "checksum": float(write_state["base"][:1024].sum()),
        }

    def run_copy():
        copied = np.copy(copy_state["base"])
        return {
            "bytes_moved": int(copy_state["base"].nbytes),
            "checksum": float(copied[:1024].sum()),
        }

    def run_transpose():
        transposed = np.transpose(transpose_state["cube"], (2, 0, 1)).copy()
        return {
            "shape": list(transposed.shape),
            "checksum": float(transposed.reshape(-1)[:1024].sum()),
        }

    def run_sort():
        sorted_values = np.sort(sort_state["values"], kind="mergesort")
        return {
            "count": int(sorted_values.size),
            "median": float(sorted_values[sorted_values.size // 2]),
        }

    def run_mask():
        selected = mask_state["values"][mask_state["mask"]]
        return {
            "selected_count": int(selected.size),
            "selection_ratio": float(selected.size / mask_state["values"].size),
        }

    return [
        BenchmarkSpec(
            category="memory_bound",
            name="write-allocate",
            description="Large contiguous float32 materialization dominated by memory writes.",
            runner=run_write,
            metadata={"bytes": int(write_bytes)},
            setup=setup_write,
            teardown=write_state.clear,
        ),
        BenchmarkSpec(
            category="memory_bound",
            name="array-copy",
            description="Contiguous float32 array copy to probe sustained memory write bandwidth.",
            runner=run_copy,
            metadata={"bytes": int(copy_bytes)},
            setup=setup_copy,
            teardown=copy_state.clear,
        ),
        BenchmarkSpec(
            category="memory_bound",
            name="transpose-copy-3d",
            description="Large non-contiguous transpose followed by a contiguous materialization.",
            runner=run_transpose,
            metadata={"bytes": int(transpose_bytes)},
            setup=setup_transpose,
            teardown=transpose_state.clear,
        ),
        BenchmarkSpec(
            category="memory_bound",
            name="float-sort",
            description="Large float32 mergesort stressing memory traffic and cache capacity.",
            runner=run_sort,
            metadata={"bytes": int(sort_bytes)},
            setup=setup_sort,
            teardown=sort_state.clear,
        ),
        BenchmarkSpec(
            category="memory_bound",
            name="boolean-mask",
            description="Boolean gather over a large float32 vector with wide memory traffic.",
            runner=run_mask,
            metadata={"bytes": int(mask_bytes)},
            setup=setup_mask,
            teardown=mask_state.clear,
        ),
    ]
