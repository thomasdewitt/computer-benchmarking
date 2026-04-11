# Benchmark Run Log

*Generated: 2026-04-10T23:11:03*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp | Machine | Total Time (s) | Result File |
| --- | --- | ---: | --- |
| 2026-03-26T16:01:15.379316+00:00 | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | 1050.00 | `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json` |
| 2026-03-26T17:31:04.562696+00:00 | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 | 1107.54 | `intel-r-xeon-r-cpu-e5-2680-v4-2-40ghz-poweredge-r430_fixed_20260326_115301.json` |
| 2026-03-26T17:31:33.744798+00:00 | Apple M1 / MacBook Air | 1048.01 | `apple-m1-macbook-air_fixed_20260326_114945.json` |
| 2026-04-11T04:44:20.633234+00:00 | AMD Ryzen 9 9950X 16-Core Processor / X870 EAGLE WIFI7 | 287.55 | `amd-ryzen-9-9950x-16-core-processor-x870-eagle-wifi7_fixed_20260410_224942.json` |

## Detailed Runs

<details>
<summary>2026-03-26T16:01:15.379316+00:00 | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | total 1,050.00 s</summary>

| Key | Value |
| --- | --- |
| Machine | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF |
| System | Linux |
| Architecture | x86_64 |
| Processor | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz |
| Model | HP ProDesk 600 G5 SFF |
| Logical Cores | 8 |
| Physical Cores | 8 |
| Python | 3.12.10 |
| Torch | 2.10.0+cpu |
| RAM Total (GB) | 33.4 |
| BLAS | blas 3.9.0 |
| LAPACK | lapack 3.9.0 |

| Category | Total Time (s) |
| --- | ---: |
| Single Threaded | 91.43 |
| Parallel | 378.49 |
| Memory Bound | 26.96 |
| Compute Bound | 553.12 |
| **Overall** | **1,050.00** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 58.67 | 3.41 | 100 |
| spectral-psd | ok | 5.21 | 4.46 | 99 |
| box-counting-dimension | ok | 16.13 | 1.36 | 100 |
| perimeter | ok | 6.54 | 1.27 | 98 |
| levy-noise | ok | 4.88 | 3.23 | 99 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 5.37 | 3.96 | 636 |
| correlation-dimension | ok | 230.39 | 1.05 | 766 |
| direct-convolution-3d | ok | 65.25 | 3.19 | 761 |
| matmul-numpy | ok | 25.75 | 5.44 | 773 |
| matmul-torch | ok | 17.69 | 5.47 | 782 |
| svd | ok | 34.03 | 1.38 | 767 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 0.22 | 2.84 | 92 |
| array-copy | ok | 0.18 | 3.14 | 90 |
| transpose-copy-3d | ok | 1.05 | 1.93 | 99 |
| float-sort | ok | 24.15 | 2.92 | 100 |
| boolean-mask | ok | 1.37 | 2.54 | 98 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 67.98 | 0.65 | 294 |
| monte-carlo-pi | ok | 133.77 | 0.57 | 781 |
| transcendentals | ok | 115.28 | 0.58 | 793 |
| n-body | ok | 144.99 | 0.60 | 784 |
| eigh | ok | 91.11 | 4.80 | 755 |

Result File: `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json`

</details>

<details>
<summary>2026-03-26T17:31:04.562696+00:00 | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 | total 1,107.54 s</summary>

| Key | Value |
| --- | --- |
| Machine | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 |
| System | Linux |
| Architecture | x86_64 |
| Processor | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz |
| Model | PowerEdge R430 |
| Logical Cores | 56 |
| Physical Cores | 28 |
| Python | 3.9.5 |
| Torch | 2.8.0+cu128 |
| RAM Total (GB) | 135.1 |
| BLAS | openblas64 0.3.23.dev |
| LAPACK | dep139810746332592 1.26.4 |

| Category | Total Time (s) |
| --- | ---: |
| Single Threaded | 368.86 |
| Parallel | 161.67 |
| Memory Bound | 43.80 |
| Compute Bound | 533.21 |
| **Overall** | **1,107.54** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 290.49 | 3.68 | 101 |
| spectral-psd | ok | 15.37 | 4.64 | 100 |
| box-counting-dimension | ok | 35.85 | 1.53 | 100 |
| perimeter | ok | 10.36 | 1.44 | 99 |
| levy-noise | ok | 16.78 | 3.41 | 100 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 10.57 | 4.17 | 1281 |
| correlation-dimension | ok | 61.95 | 1.18 | 4833 |
| direct-convolution-3d | ok | 24.14 | 3.36 | 4400 |
| matmul-numpy | ok | 11.86 | 5.61 | 5173 |
| matmul-torch | ok | 8.18 | 5.64 | 2669 |
| svd | ok | 44.98 | 1.55 | 4814 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 1.36 | 3.20 | 98 |
| array-copy | ok | 1.21 | 3.51 | 100 |
| transpose-copy-3d | ok | 2.52 | 2.09 | 101 |
| float-sort | ok | 36.21 | 3.06 | 100 |
| boolean-mask | ok | 2.50 | 2.67 | 100 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 15.94 | 0.78 | 1728 |
| monte-carlo-pi | ok | 68.68 | 0.69 | 5010 |
| transcendentals | ok | 305.16 | 0.69 | 2733 |
| n-body | ok | 43.95 | 0.70 | 4880 |
| eigh | ok | 99.49 | 4.88 | 4397 |

Result File: `intel-r-xeon-r-cpu-e5-2680-v4-2-40ghz-poweredge-r430_fixed_20260326_115301.json`

</details>

<details>
<summary>2026-03-26T17:31:33.744798+00:00 | Apple M1 / MacBook Air | total 1,048.01 s</summary>

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
| Single Threaded | 85.49 |
| Parallel | 439.66 |
| Memory Bound | 32.79 |
| Compute Bound | 490.07 |
| **Overall** | **1,048.01** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 57.78 | 3.19 | 99 |
| spectral-psd | ok | 6.62 | 3.34 | 87 |
| box-counting-dimension | ok | 10.75 | 1.39 | 99 |
| perimeter | ok | 6.41 | 1.80 | 92 |
| levy-noise | ok | 3.94 | 3.61 | 99 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 7.47 | 3.68 | 192 |
| correlation-dimension | ok | 266.51 | 1.21 | 788 |
| direct-convolution-3d | ok | 55.05 | 3.23 | 775 |
| matmul-numpy | ok | 36.46 | 2.70 | 751 |
| matmul-torch | ok | 36.49 | 3.02 | 755 |
| svd | ok | 37.67 | 0.94 | 772 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 0.23 | 2.14 | 95 |
| array-copy | ok | 0.16 | 2.68 | 90 |
| transpose-copy-3d | ok | 0.84 | 1.47 | 100 |
| float-sort | ok | 30.06 | 2.57 | 100 |
| boolean-mask | ok | 1.49 | 2.19 | 99 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 94.49 | 0.30 | 298 |
| monte-carlo-pi | ok | 99.06 | 0.31 | 791 |
| transcendentals | ok | 106.96 | 0.46 | 651 |
| n-body | ok | 115.21 | 0.48 | 784 |
| eigh | ok | 74.35 | 3.76 | 772 |

Result File: `apple-m1-macbook-air_fixed_20260326_114945.json`

</details>

<details>
<summary>2026-04-11T04:44:20.633234+00:00 | AMD Ryzen 9 9950X 16-Core Processor / X870 EAGLE WIFI7 | total 287.55 s</summary>

| Key | Value |
| --- | --- |
| Machine | AMD Ryzen 9 9950X 16-Core Processor / X870 EAGLE WIFI7 |
| System | Linux |
| Architecture | x86_64 |
| Processor | AMD Ryzen 9 9950X 16-Core Processor |
| Model | X870 EAGLE WIFI7 |
| Logical Cores | 32 |
| Physical Cores | 16 |
| Python | 3.14.3 |
| Torch | 2.11.0+cpu |
| RAM Total (GB) | 64.9 |
| BLAS | scipy-openblas 0.3.31.188.0 |

| Category | Total Time (s) |
| --- | ---: |
| Single Threaded | 79.87 |
| Parallel | 75.86 |
| Memory Bound | 20.01 |
| Compute Bound | 111.82 |
| **Overall** | **287.55** |

### Single Threaded

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| structure-function | ok | 27.34 | 3.45 | 100 |
| spectral-psd | ok | 2.42 | 4.50 | 99 |
| box-counting-dimension | ok | 43.32 | 1.40 | 100 |
| perimeter | ok | 4.38 | 1.31 | 104 |
| levy-noise | ok | 2.40 | 3.21 | 99 |

### Parallel

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| fif-nd-torch | ok | 2.88 | 3.78 | 1298 |
| correlation-dimension | ok | 41.65 | 1.08 | 3058 |
| direct-convolution-3d | ok | 7.69 | 3.28 | 2947 |
| matmul-numpy | ok | 3.57 | 5.56 | 3169 |
| matmul-torch | ok | 5.72 | 5.66 | 1500 |
| svd | ok | 14.36 | 1.57 | 3019 |

### Memory Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| write-allocate | ok | 0.13 | 2.78 | 87 |
| array-copy | ok | 0.10 | 2.90 | 100 |
| transpose-copy-3d | ok | 0.20 | 2.14 | 80 |
| float-sort | ok | 18.64 | 3.12 | 100 |
| boolean-mask | ok | 0.95 | 2.72 | 99 |

### Compute Bound

| Benchmark | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --- | --- | ---: | ---: | ---: |
| mandelbrot | ok | 11.57 | 0.84 | 984 |
| monte-carlo-pi | ok | 7.56 | 0.76 | 3105 |
| transcendentals | ok | 27.60 | 0.77 | 3151 |
| n-body | ok | 30.36 | 0.78 | 3115 |
| eigh | ok | 34.72 | 4.99 | 2998 |

Result File: `amd-ryzen-9-9950x-16-core-processor-x870-eagle-wifi7_fixed_20260410_224942.json`

</details>
