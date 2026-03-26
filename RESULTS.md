# Benchmark Run Log

*Generated: 2026-03-25T17:49:12*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp | Machine | Total Time (s) | Result File |
| --- | --- | ---: | --- |
| 2026-03-25T23:30:43.338605+00:00 | Apple M1 / MacBook Air | 1069.64 | `apple-m1-macbook-air_fixed_20260325_174912.json` |

## Detailed Runs

<details>
<summary>2026-03-25T23:30:43.338605+00:00 | Apple M1 / MacBook Air | total 1,069.64 s</summary>

| Key | Value |
| --- | --- |
| Machine | Apple M1 / MacBook Air |
| System | Darwin |
| Architecture | arm64 |
| Processor | Apple M1 |
| Chip | Apple M1 |
| Model | MacBook Air |
| Logical Cores | 8 |
| Physical Cores | 8 |
| Python | 3.11.14 |
| Torch | 2.5.1 |
| RAM Total (GB) | 8.6 |
| BLAS | openblas 0.3.30 |

| Category | Total Time (s) |
| --- | ---: |
| Single Threaded | 84.09 |
| Parallel | 454.23 |
| Memory Bound | 32.79 |
| Compute Bound | 498.52 |
| **Overall** | **1,069.64** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 57.92 | 3.44 | 100 |
| spectral-psd | ok | 5.69 | 3.80 | 88 |
| box-counting-dimension | ok | 10.45 | 1.48 | 100 |
| perimeter | ok | 6.20 | 1.85 | 93 |
| levy-noise | ok | 3.83 | 3.80 | 100 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 7.13 | 4.39 | 196 |
| correlation-dimension | ok | 269.36 | 1.26 | 777 |
| direct-convolution-3d | ok | 64.20 | 3.65 | 780 |
| matmul-numpy | ok | 41.75 | 2.32 | 681 |
| matmul-torch | ok | 36.09 | 3.90 | 770 |
| svd | ok | 35.69 | 0.97 | 783 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 0.19 | 2.28 | 90 |
| array-copy | ok | 0.15 | 2.69 | 93 |
| transpose-copy-3d | ok | 0.84 | 1.54 | 95 |
| float-sort | ok | 30.10 | 2.72 | 100 |
| boolean-mask | ok | 1.50 | 2.34 | 97 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 94.66 | 0.45 | 297 |
| monte-carlo-pi | ok | 99.95 | 0.56 | 784 |
| transcendentals | ok | 109.61 | 0.58 | 645 |
| n-body | ok | 117.28 | 0.60 | 785 |
| eigh | ok | 77.03 | 4.16 | 773 |

Result File: `apple-m1-macbook-air_fixed_20260325_174912.json`

</details>
