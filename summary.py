#!/usr/bin/env python3
from __future__ import annotations

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

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    generate_summary()
