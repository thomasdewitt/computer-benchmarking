# Benchmark Run Log

*Generated: 2026-03-25T16:00:16*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp                        | Machine                | Total Time (s) | Result File                                      |
| -------------------------------- | ---------------------- | --------------:| ------------------------------------------------ |
| 2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | 1684.37        | `apple-m1-macbook-air_full_20260325_141656.json` |
| 2026-03-25T21:33:52.670110+00:00 | x86_64                 | 1276.45        | `x86-64_default_20260325_160016.json`            |

## Detailed Runs

<details>
<summary>2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | total 1,684.37 s</summary>

| Key            | Value                  |
| -------------- | ---------------------- |
| Machine        | Apple M1 / MacBook Air |
| System         | Darwin                 |
| Architecture   | arm64                  |
| Processor      | Apple M1               |
| Chip           | Apple M1               |
| Model          | MacBook Air            |
| Logical Cores  | 8                      |
| Physical Cores | 8                      |
| Python         | 3.11.14                |
| Torch          | 2.5.1                  |
| RAM Total (GB) | 8.6                    |

| Category        | Total Time (s) |
| --------------- | --------------:|
| Single Threaded | 702.60         |
| Parallel        | 460.12         |
| Memory Bound    | 32.74          |
| Compute Bound   | 488.91         |
| **Overall**     | **1,684.37**   |

### Single Threaded

| Benchmark              | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| ---------------------- | ------ | --------:| -------------:| -----------:|
| structure-function     | ok     | 604.55   | 5.87          | 46          |
| spectral-psd           | ok     | 48.90    | 4.86          | 42          |
| box-counting-dimension | ok     | 24.01    | 2.58          | 100         |
| perimeter              | ok     | 12.68    | 2.36          | 95          |
| levy-noise             | ok     | 12.46    | 4.44          | 79          |

### Parallel

| Benchmark             | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --------------------- | ------ | --------:| -------------:| -----------:|
| fif-nd-torch          | ok     | 17.09    | 5.31          | 178         |
| correlation-dimension | ok     | 270.26   | 1.04          | 773         |
| direct-convolution-3d | ok     | 63.40    | 3.46          | 783         |
| matmul-numpy          | ok     | 37.60    | 2.57          | 729         |
| matmul-torch          | ok     | 35.38    | 3.89          | 773         |
| svd                   | ok     | 36.40    | 0.94          | 777         |

### Memory Bound

| Benchmark         | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| ----------------- | ------ | --------:| -------------:| -----------:|
| write-allocate    | ok     | 0.20     | 2.27          | 89          |
| array-copy        | ok     | 0.17     | 2.58          | 100         |
| transpose-copy-3d | ok     | 0.85     | 1.50          | 96          |
| float-sort        | ok     | 30.04    | 2.50          | 100         |
| boolean-mask      | ok     | 1.49     | 2.13          | 97          |

### Compute Bound

| Benchmark       | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --------------- | ------ | --------:| -------------:| -----------:|
| mandelbrot      | ok     | 94.55    | 0.29          | 296         |
| monte-carlo-pi  | ok     | 99.97    | 0.30          | 781         |
| transcendentals | ok     | 107.18   | 0.33          | 646         |
| n-body          | ok     | 114.25   | 0.47          | 787         |
| eigh            | ok     | 72.96    | 4.30          | 782         |

Result File: `apple-m1-macbook-air_full_20260325_141656.json`

</details>

<details>
<summary>2026-03-25T21:33:52.670110+00:00 | x86_64 | total 1,276.45 s</summary>

| Key            | Value       |
| -------------- | ----------- |
| Machine        | x86_64      |
| System         | Linux       |
| Architecture   | x86_64      |
| Processor      | x86_64      |
| Logical Cores  | 56          |
| Physical Cores | 28          |
| Python         | 3.9.5       |
| Torch          | 2.8.0+cu128 |
| RAM Total (GB) | 135.1       |

| Category        | Total Time (s) |
| --------------- | --------------:|
| Single Threaded | 316.47         |
| Parallel        | 144.11         |
| Memory Bound    | 402.54         |
| Compute Bound   | 413.33         |
| **Overall**     | **1,276.45**   |

### Single Threaded

| Benchmark              | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| ---------------------- | ------ | --------:| -------------:| -----------:|
| structure-function     | ok     | 264.87   | 3.69          | 101         |
| spectral-psd           | ok     | 14.52    | 4.74          | 100         |
| box-counting-dimension | ok     | 16.77    | 1.21          | 100         |
| perimeter              | ok     | 5.00     | 1.08          | 94          |
| levy-noise             | ok     | 15.32    | 3.46          | 101         |

### Parallel

| Benchmark             | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --------------------- | ------ | --------:| -------------:| -----------:|
| fif-nd-torch          | ok     | 10.53    | 4.22          | 1422        |
| correlation-dimension | ok     | 60.30    | 1.29          | 5034        |
| direct-convolution-3d | ok     | 23.43    | 3.47          | 4692        |
| matmul-numpy          | ok     | 8.69     | 5.74          | 5486        |
| matmul-torch          | ok     | 7.01     | 5.77          | 2674        |
| svd                   | ok     | 34.14    | 1.68          | 5063        |

### Memory Bound

| Benchmark         | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| ----------------- | ------ | --------:| -------------:| -----------:|
| write-allocate    | ok     | 4.79     | 9.37          | 100         |
| array-copy        | ok     | 6.48     | 17.95         | 101         |
| transpose-copy-3d | ok     | 18.47    | 9.43          | 100         |
| float-sort        | ok     | 355.67   | 22.33         | 100         |
| boolean-mask      | ok     | 17.13    | 15.88         | 100         |

### Compute Bound

| Benchmark       | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --------------- | ------ | --------:| -------------:| -----------:|
| mandelbrot      | ok     | 15.24    | 0.93          | 1786        |
| monte-carlo-pi  | ok     | 65.97    | 0.85          | 5258        |
| transcendentals | ok     | 211.79   | 0.86          | 3417        |
| n-body          | ok     | 41.27    | 0.87          | 5340        |
| eigh            | ok     | 79.07    | 5.08          | 4781        |

Result File: `x86-64_default_20260325_160016.json`

</details>
