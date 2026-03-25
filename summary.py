#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from benchmarks.harness import CATEGORY_ORDER
from report import (
    compute_scores,
    latest_runs_by_machine_profile,
    load_result_files,
    machine_label,
    run_timestamp,
)


def _slugify(value: str) -> str:
    return value.replace(" ", "-").replace("_", "-").lower()


def _plot_profile_scores(
    results_dir: Path,
    *,
    profile: str,
    rows: list[tuple[str, float]],
    score_key: str,
    title: str,
) -> str:
    plot_dir = results_dir / "plots"
    plot_dir.mkdir(parents=True, exist_ok=True)
    output = plot_dir / f"summary-{_slugify(profile)}-{_slugify(score_key)}.png"

    ordered = sorted(rows, key=lambda item: item[1], reverse=True)
    labels = [label for label, _ in ordered]
    values = [value for _, value in ordered]

    fig, ax = plt.subplots(figsize=(9, max(2.8, 0.45 * len(labels))))
    ax.barh(labels, values, color="#2c7fb8")
    ax.invert_yaxis()
    ax.set_xlabel("Score (higher = faster)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output, dpi=160)
    plt.close(fig)
    return str(output.relative_to(results_dir.parent))


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

    latest_runs = latest_runs_by_machine_profile(payloads)
    by_profile: dict[str, list[dict]] = {}
    for (profile, _machine_key), payload in latest_runs.items():
        by_profile.setdefault(profile, []).append(payload)

    lines = [
        "# Benchmark Summary",
        "",
        f"*Generated: {datetime.now().isoformat(timespec='seconds')}*",
        "",
        "This summary compares the latest saved run for each machine within each profile.",
        "",
    ]

    for profile in sorted(by_profile):
        runs = sorted(
            by_profile[profile],
            key=lambda payload: compute_scores(payload["results"]).get("_overall", 0.0),
            reverse=True,
        )
        scores_by_run = {id(payload): compute_scores(payload["results"]) for payload in runs}

        lines.extend(
            [
                f"## Profile `{profile}`",
                "",
                "| Machine | Overall | Single Threaded | Parallel | Memory Bound | Compute Bound | Latest Run | Result File |",
                "| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
            ]
        )

        for payload in runs:
            scores = scores_by_run[id(payload)]
            lines.append(
                f"| {machine_label(payload)} | {scores.get('_overall', 0.0):,.0f} | "
                f"{scores.get('_category_single_threaded', 0.0):,.0f} | "
                f"{scores.get('_category_parallel', 0.0):,.0f} | "
                f"{scores.get('_category_memory_bound', 0.0):,.0f} | "
                f"{scores.get('_category_compute_bound', 0.0):,.0f} | "
                f"{run_timestamp(payload)} | `{payload['_path'].name}` |"
            )

        lines.append("")

        overall_chart = _plot_profile_scores(
            results_dir,
            profile=profile,
            rows=[
                (machine_label(payload), scores_by_run[id(payload)].get("_overall", 0.0))
                for payload in runs
            ],
            score_key="overall",
            title=f"{profile.title()} Overall Scores",
        )
        lines.extend([f"![{profile} overall]({overall_chart})", ""])

        for category in CATEGORY_ORDER:
            chart_path = _plot_profile_scores(
                results_dir,
                profile=profile,
                rows=[
                    (
                        machine_label(payload),
                        scores_by_run[id(payload)].get(f"_category_{category}", 0.0),
                    )
                    for payload in runs
                ],
                score_key=category,
                title=f"{profile.title()} {category.replace('_', ' ').title()} Scores",
            )
            lines.extend([f"![{profile} {category}]({chart_path})", ""])

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    generate_summary()
