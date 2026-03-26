#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from pathlib import Path

from benchmarks.harness import CATEGORY_ORDER
from report import (
    category_total_times,
    latest_runs_by_machine,
    load_result_files,
    machine_label,
    run_timestamp,
)


def _machine_columns(runs: list[dict]) -> list[tuple[str, dict]]:
    counts: dict[str, int] = defaultdict(int)
    columns: list[tuple[str, dict]] = []
    for payload in runs:
        label = machine_label(payload)
        counts[label] += 1
        if counts[label] > 1:
            label = f"{label} ({counts[label]})"
        columns.append((label, payload))
    return columns


def _results_by_name(payload: dict) -> dict[str, dict]:
    return {row["name"]: row for row in payload["results"] if row["status"] == "ok"}


def _benchmark_rows(runs: list[dict]) -> list[tuple[str, str]]:
    ordered: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for category in CATEGORY_ORDER:
        for payload in runs:
            for row in payload["results"]:
                key = (row["category"], row["name"])
                if row["category"] != category or key in seen:
                    continue
                seen.add(key)
                ordered.append(key)
    return ordered


def generate_summary(
    results_dir: str | Path = "results",
    output_path: str | Path = "SUMMARY.md",
) -> Path:
    results_dir = Path(results_dir)
    output_path = Path(output_path)
    payloads = load_result_files(results_dir)

    if not payloads:
        output_path.write_text("# Benchmark Summary\n\nNo result files found.\n", encoding="utf-8")
        return output_path

    latest_runs = latest_runs_by_machine(payloads)
    runs = sorted(
        latest_runs.values(),
        key=lambda payload: category_total_times(payload["results"]).get("overall", 0.0),
    )
    machine_columns = _machine_columns(runs)
    benchmark_rows = _benchmark_rows(runs)

    lines = [
        "# Benchmark Summary",
        "",
        f"*Generated: {datetime.now().isoformat(timespec='seconds')}*",
        "",
        "This summary compares the latest saved run for each machine using total wall time.",
        "",
        "## Time Summary",
        "",
        "| Machine | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run | Result File |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]

    for payload in runs:
        totals = category_total_times(payload["results"])
        lines.append(
            f"| {machine_label(payload)} | {totals.get('overall', 0.0):,.2f} | "
            f"{totals.get('single_threaded', 0.0):,.2f} | "
            f"{totals.get('parallel', 0.0):,.2f} | "
            f"{totals.get('memory_bound', 0.0):,.2f} | "
            f"{totals.get('compute_bound', 0.0):,.2f} | "
            f"{run_timestamp(payload)} | `{payload['_path'].name}` |"
        )

    lines.extend(
        [
            "",
            "## Benchmark Matrix",
            "",
            "Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.",
            "",
        ]
    )

    header = ["Benchmark", "Workflow Type", *[label for label, _ in machine_columns]]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---", "---", *(["---:"] * len(machine_columns))]) + " |")

    run_results = {id(payload): _results_by_name(payload) for payload in runs}
    for category, benchmark_name in benchmark_rows:
        row = [benchmark_name, category.replace("_", " ").title()]
        for _, payload in machine_columns:
            result = run_results[id(payload)].get(benchmark_name)
            row.append(f"{result['wall_time_sec']:,.2f}" if result is not None else "")
        lines.append("| " + " | ".join(row) + " |")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    generate_summary()
