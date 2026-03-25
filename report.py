#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from benchmarks.harness import machine_label_from_system_info, machine_slug_from_system_info


def load_result_files(results_dir: str | Path) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for path in sorted(Path(results_dir).glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["_path"] = path
        payloads.append(payload)
    return payloads


def category_total_times(rows: list[dict[str, Any]]) -> dict[str, float]:
    from benchmarks.harness import CATEGORY_ORDER

    totals: dict[str, float] = {}

    overall = 0.0
    for row in rows:
        if row["status"] != "ok" or row["wall_time_sec"] <= 0:
            continue
        overall += float(row["wall_time_sec"])
        key = row["category"]
        totals[key] = totals.get(key, 0.0) + float(row["wall_time_sec"])

    for category in CATEGORY_ORDER:
        totals.setdefault(category, 0.0)
    totals["overall"] = overall
    return totals


def machine_label(payload: dict[str, Any]) -> str:
    return machine_label_from_system_info(payload["system_info"])


def machine_key(payload: dict[str, Any]) -> tuple[str, str, str]:
    system_info = payload["system_info"]
    return (
        machine_slug_from_system_info(system_info),
        str(system_info.get("system") or "unknown"),
        str(system_info.get("memory_total_bytes") or "unknown"),
    )


def run_timestamp(payload: dict[str, Any]) -> str:
    return str(payload["system_info"].get("generated_at") or payload["_path"].stem)


def run_profile(payload: dict[str, Any]) -> str:
    return str(payload.get("run_metadata", {}).get("profile", "default"))


def run_total_time(payload: dict[str, Any]) -> float:
    return float(
        sum(row["wall_time_sec"] for row in payload["results"] if row["status"] == "ok")
    )


def latest_runs_by_machine(
    payloads: list[dict[str, Any]],
) -> dict[tuple[str, str, str], dict[str, Any]]:
    latest: dict[tuple[str, str, str], dict[str, Any]] = {}
    for payload in payloads:
        key = machine_key(payload)
        current = latest.get(key)
        if current is None or run_timestamp(payload) > run_timestamp(current):
            latest[key] = payload
    return latest


def _format_time_summary(totals: dict[str, float]) -> str:
    from benchmarks.harness import CATEGORY_ORDER

    lines = [
        "| Category | Total Time (s) |",
        "| --- | ---: |",
    ]
    for category in CATEGORY_ORDER:
        lines.append(f"| {category.replace('_', ' ').title()} | {totals.get(category, 0.0):,.2f} |")
    lines.append(f"| **Overall** | **{totals.get('overall', 0.0):,.2f}** |")
    return "\n".join(lines)


def _format_system_table(system_info: dict[str, Any]) -> str:
    rows = [
        ("Machine", machine_label_from_system_info(system_info)),
        ("System", system_info["system"]),
        ("Architecture", system_info["machine"]),
        ("Processor", system_info["processor"]),
    ]
    if system_info.get("chip"):
        rows.append(("Chip", system_info["chip"]))
    if system_info.get("model_name"):
        rows.append(("Model", system_info["model_name"]))
    rows.extend(
        [
            ("Logical Cores", system_info["logical_cores"]),
            ("Physical Cores", system_info["physical_cores"]),
            ("Python", system_info["python"]),
            ("Torch", system_info["torch_version"]),
            ("RAM Total (GB)", f"{system_info['memory_total_bytes'] / 1e9:.1f}"),
        ]
    )
    lines = ["| Key | Value |", "| --- | --- |"]
    for key, value in rows:
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def _format_results_table(rows: list[dict[str, Any]]) -> str:
    lines = [
        "| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['name']} | {row['status']} | {row['wall_time_sec']:.2f} | "
            f"{row['peak_mem_gb']:.2f} | {row['avg_cpu_pct']:.0f} |"
        )
    return "\n".join(lines)


def generate_report(
    results_dir: str | Path = "results",
    output_path: str | Path = "RESULTS.md",
) -> Path:
    from benchmarks.harness import CATEGORY_ORDER

    output_path = Path(output_path)
    payloads = load_result_files(results_dir)

    if not payloads:
        output_path.write_text("# Benchmark Run Log\n\nNo result files found.\n", encoding="utf-8")
        return output_path

    payloads = sorted(
        payloads,
        key=lambda payload: (run_timestamp(payload), payload["_path"].name),
    )

    lines = [
        "# Benchmark Run Log",
        "",
        f"*Generated: {datetime.now().isoformat(timespec='seconds')}*",
        "",
        "This file is an append-only view over all saved JSON result files.",
        "",
        "## Run Index",
        "",
        "| Timestamp | Machine | Total Time (s) | Result File |",
        "| --- | --- | ---: | --- |",
    ]

    for payload in payloads:
        lines.append(
            f"| {run_timestamp(payload)} | {machine_label(payload)} | "
            f"{run_total_time(payload):.2f} | `{payload['_path'].name}` |"
        )

    lines.extend(["", "## Detailed Runs", ""])

    for payload in payloads:
        totals = category_total_times(payload["results"])
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in payload["results"]:
            grouped[row["category"]].append(row)

        lines.extend(
            [
                "<details>",
                (
                    f"<summary>{run_timestamp(payload)} | {machine_label(payload)} | "
                    f"total {totals.get('overall', 0.0):,.2f} s</summary>"
                ),
                "",
                _format_system_table(payload["system_info"]),
                "",
                _format_time_summary(totals),
                "",
            ]
        )

        for category in CATEGORY_ORDER:
            rows = grouped.get(category, [])
            if not rows:
                continue
            lines.extend(
                [
                    f"### {category.replace('_', ' ').title()}",
                    "",
                    _format_results_table(rows),
                    "",
                ]
            )

        lines.extend(
            [
                f"Result File: `{payload['_path'].name}`",
                "",
                "</details>",
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    generate_report()
