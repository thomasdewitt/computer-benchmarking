# Benchmark Run Log

*Generated: 2026-03-25T14:24:46*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp                        | Machine                | Profile | Overall Score | Total Time (s) | Result File                                      |
| -------------------------------- | ---------------------- | ------- | -------------:| --------------:| ------------------------------------------------ |
| 2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | full    | 47            | 1684.4         | `apple-m1-macbook-air_full_20260325_141656.json` |

## Detailed Runs

<details>
<summary>2026-03-25T19:47:16.322353+00:00 | Apple M1 / MacBook Air | full | overall 47</summary>

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

| Category        | Score  |
| --------------- | ------:|
| Single Threaded | 25     |
| Parallel        | 20     |
| Memory Bound    | 957    |
| Compute Bound   | 10     |
| **Overall**     | **47** |

### Single Threaded

| Benchmark              | Status | Time (s) | Score | Peak Mem (GB) | Avg CPU (%) |
| ---------------------- | ------ | --------:| -----:| -------------:| -----------:|
| structure-function     | ok     | 604.55   | 2     | 5.87          | 46          |
| spectral-psd           | ok     | 48.90    | 20    | 4.86          | 42          |
| box-counting-dimension | ok     | 24.01    | 42    | 2.58          | 100         |
| perimeter              | ok     | 12.68    | 79    | 2.36          | 95          |
| levy-noise             | ok     | 12.46    | 80    | 4.44          | 79          |

### Parallel

| Benchmark             | Status | Time (s) | Score | Peak Mem (GB) | Avg CPU (%) |
| --------------------- | ------ | --------:| -----:| -------------:| -----------:|
| fif-nd-torch          | ok     | 17.09    | 59    | 5.31          | 178         |
| correlation-dimension | ok     | 270.26   | 4     | 1.04          | 773         |
| direct-convolution-3d | ok     | 63.40    | 16    | 3.46          | 783         |
| matmul-numpy          | ok     | 37.60    | 27    | 2.57          | 729         |
| matmul-torch          | ok     | 35.38    | 28    | 3.89          | 773         |
| svd                   | ok     | 36.40    | 27    | 0.94          | 777         |

### Memory Bound

| Benchmark         | Status | Time (s) | Score | Peak Mem (GB) | Avg CPU (%) |
| ----------------- | ------ | --------:| -----:| -------------:| -----------:|
| write-allocate    | ok     | 0.20     | 5077  | 2.27          | 89          |
| array-copy        | ok     | 0.17     | 6028  | 2.58          | 100         |
| transpose-copy-3d | ok     | 0.85     | 1176  | 1.50          | 96          |
| float-sort        | ok     | 30.04    | 33    | 2.50          | 100         |
| boolean-mask      | ok     | 1.49     | 670   | 2.13          | 97          |

### Compute Bound

| Benchmark       | Status | Time (s) | Score | Peak Mem (GB) | Avg CPU (%) |
| --------------- | ------ | --------:| -----:| -------------:| -----------:|
| mandelbrot      | ok     | 94.55    | 11    | 0.29          | 296         |
| monte-carlo-pi  | ok     | 99.97    | 10    | 0.30          | 781         |
| transcendentals | ok     | 107.18   | 9     | 0.33          | 646         |
| n-body          | ok     | 114.25   | 9     | 0.47          | 787         |
| eigh            | ok     | 72.96    | 14    | 4.30          | 782         |

Result File: `apple-m1-macbook-air_full_20260325_141656.json`

</details>
