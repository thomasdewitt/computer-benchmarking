# Benchmarking Suite

Comprehensive CPU benchmark suite for local scientific workloads using only:

- `numpy`
- `scipy`
- `numba`
- `torch` (CPU)
- `matplotlib`
- `psutil`

The suite reproduces the needed `scaleinvariance` and `objscale` algorithms locally instead of importing those packages. It covers:

- `single_threaded`
- `parallel`
- `memory_bound`
- `compute_bound`

## Usage

```bash
python run.py
python run.py --category parallel
python run.py --list
python run.py --output results
python summary.py
```

The suite now uses a single fixed workload path based on the historical M1 `full` run. Every machine executes the same benchmark sizes, including fixed memory-bound byte counts. The FIF benchmark uses a fixed `8192 x 8192` field.

## Outputs

- append-only run log in `RESULTS.md`
- machine comparison summary in `SUMMARY.md`
- JSON runs in `results/` with sanitized machine metadata only

## Layout

```text
benchmarking/
├── README.md
├── benchmark.py
├── pyproject.toml
├── requirements.txt
├── run.py
├── benchmarks/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── compute_bound.py
│   ├── harness.py
│   ├── memory_bound.py
│   ├── parallel.py
│   └── single_threaded.py
├── report.py
└── results/
```
