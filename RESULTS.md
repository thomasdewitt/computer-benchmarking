# Benchmark Run Log

*Generated: 2026-03-25T15:32:35*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp | Machine | Total Time (s) | Result File |
| --- | --- | ---: | --- |
| 2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | 1684.37 | `apple-m1-macbook-air_full_20260325_141656.json` |
| 2026-03-25T21:14:00.740117+00:00 | Apple M1 / MacBook Air | 1063.07 | `apple-m1-macbook-air_default_20260325_153235.json` |

## Detailed Runs

<details>
<summary>2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | total 1,684.37 s</summary>

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

| Category | Total Time (s) |
| --- | ---: |
| Single Threaded | 702.60 |
| Parallel | 460.12 |
| Memory Bound | 32.74 |
| Compute Bound | 488.91 |
| **Overall** | **1,684.37** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 604.55 | 5.87 | 46 |
| spectral-psd | ok | 48.90 | 4.86 | 42 |
| box-counting-dimension | ok | 24.01 | 2.58 | 100 |
| perimeter | ok | 12.68 | 2.36 | 95 |
| levy-noise | ok | 12.46 | 4.44 | 79 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 17.09 | 5.31 | 178 |
| correlation-dimension | ok | 270.26 | 1.04 | 773 |
| direct-convolution-3d | ok | 63.40 | 3.46 | 783 |
| matmul-numpy | ok | 37.60 | 2.57 | 729 |
| matmul-torch | ok | 35.38 | 3.89 | 773 |
| svd | ok | 36.40 | 0.94 | 777 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 0.20 | 2.27 | 89 |
| array-copy | ok | 0.17 | 2.58 | 100 |
| transpose-copy-3d | ok | 0.85 | 1.50 | 96 |
| float-sort | ok | 30.04 | 2.50 | 100 |
| boolean-mask | ok | 1.49 | 2.13 | 97 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 94.55 | 0.29 | 296 |
| monte-carlo-pi | ok | 99.97 | 0.30 | 781 |
| transcendentals | ok | 107.18 | 0.33 | 646 |
| n-body | ok | 114.25 | 0.47 | 787 |
| eigh | ok | 72.96 | 4.30 | 782 |

Result File: `apple-m1-macbook-air_full_20260325_141656.json`

</details>

<details>
<summary>2026-03-25T21:14:00.740117+00:00 | Apple M1 / MacBook Air | total 1,063.07 s</summary>

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

| Category | Total Time (s) |
| --- | ---: |
| Single Threaded | 74.88 |
| Parallel | 446.56 |
| Memory Bound | 53.75 |
| Compute Bound | 487.88 |
| **Overall** | **1,063.07** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 56.80 | 3.44 | 100 |
| spectral-psd | ok | 5.87 | 4.40 | 87 |
| box-counting-dimension | ok | 5.12 | 1.07 | 100 |
| perimeter | ok | 3.33 | 1.19 | 96 |
| levy-noise | ok | 3.77 | 3.53 | 99 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 6.50 | 4.22 | 204 |
| correlation-dimension | ok | 272.28 | 1.33 | 776 |
| direct-convolution-3d | ok | 54.90 | 3.71 | 784 |
| matmul-numpy | ok | 36.56 | 2.56 | 752 |
| matmul-torch | ok | 39.12 | 5.06 | 726 |
| svd | ok | 37.20 | 0.99 | 776 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 0.35 | 3.85 | 91 |
| array-copy | ok | 2.82 | 4.02 | 31 |
| transpose-copy-3d | ok | 1.30 | 2.19 | 98 |
| float-sort | ok | 46.98 | 3.66 | 100 |
| boolean-mask | ok | 2.29 | 3.07 | 99 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 94.58 | 0.21 | 297 |
| monte-carlo-pi | ok | 99.24 | 0.22 | 788 |
| transcendentals | ok | 105.93 | 0.37 | 653 |
| n-body | ok | 114.27 | 0.39 | 786 |
| eigh | ok | 73.86 | 4.34 | 778 |

Result File: `apple-m1-macbook-air_default_20260325_153235.json`

</details>
