# Benchmark Run Log

*Generated: 2026-03-25T15:00:57*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp | Machine | Total Time (s) | Result File |
| --- | --- | ---: | --- |
| 2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | 1684.37 | `apple-m1-macbook-air_full_20260325_141656.json` |

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
