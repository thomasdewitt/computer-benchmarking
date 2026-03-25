#!/usr/bin/env python3
from __future__ import annotations

import argparse
from importlib import import_module
from pathlib import Path
from typing import Iterable

from benchmarks import CATEGORY_ORDER
from benchmarks.harness import (
    BenchmarkResult,
    default_results_path,
    get_system_info,
    print_measurement_assessment,
    print_summary_table,
    print_system_info,
    run_benchmark,
    save_results,
)
from report import generate_report
from summary import generate_summary


CATEGORY_MODULES = {
    "single_threaded": "benchmarks.single_threaded",
    "parallel": "benchmarks.parallel",
    "memory_bound": "benchmarks.memory_bound",
    "compute_bound": "benchmarks.compute_bound",
}

RUN_PROFILE = "default"

def load_specs(categories: Iterable[str], system_info: dict) -> list:
    specs = []
    for category in categories:
        module = import_module(CATEGORY_MODULES[category])
        specs.extend(module.get_benchmarks(system_info))
    return specs


def list_benchmarks(system_info: dict) -> None:
    for category in CATEGORY_ORDER:
        print(category)
        module = import_module(CATEGORY_MODULES[category])
        for spec in module.get_benchmarks(system_info):
            print(f"  - {spec.name}: {spec.description}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CPU benchmark suite")
    parser.add_argument(
        "--category",
        action="append",
        choices=CATEGORY_ORDER,
        help="Run only the selected category. May be passed multiple times.",
    )
    parser.add_argument(
        "--output",
        default="results",
        help="Directory for JSON result files and plots.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available benchmarks and exit.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip report generation after writing JSON results.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    categories = args.category or CATEGORY_ORDER
    system_info = get_system_info()

    if args.list:
        list_benchmarks(system_info)
        return 0

    print_system_info(system_info)
    specs = load_specs(categories, system_info)
    results: list[BenchmarkResult] = []

    for spec in specs:
        results.append(run_benchmark(spec))

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = default_results_path(output_dir, RUN_PROFILE, system_info)
    saved_path = save_results(
        results,
        result_path,
        system_info=system_info,
        run_metadata={
            "profile": RUN_PROFILE,
            "categories": list(categories),
            "output_dir": str(output_dir),
        },
    )
    print(f"Saved results to {saved_path}")
    print()
    print_summary_table(results)
    print_measurement_assessment(
        results,
        logical_cores=system_info["logical_cores"],
        profile=RUN_PROFILE,
    )

    if not args.no_report:
        report_path = generate_report(results_dir=output_dir, output_path=Path("RESULTS.md"))
        summary_path = generate_summary(results_dir=output_dir, output_path=Path("SUMMARY.md"))
        print(f"Updated report at {report_path}")
        print(f"Updated summary at {summary_path}")

    failures = [result for result in results if result.status != "ok"]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
