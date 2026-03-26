# Benchmark Run Log

*Generated: 2026-03-26T10:19:37*

This file is an append-only view over all saved JSON result files.

## Run Index

| Timestamp                        | Machine                                                         | Total Time (s) | Result File                                                                            |
| -------------------------------- | --------------------------------------------------------------- | --------------:| -------------------------------------------------------------------------------------- |
| 2026-03-26T16:01:15.379316+00:00 | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | 1050.00        | `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json` |

## Detailed Runs

<details>
<summary>2026-03-26T16:01:15.379316+00:00 | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | total 1,050.00 s</summary>

| Key            | Value                                                           |
| -------------- | --------------------------------------------------------------- |
| Machine        | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF |
| System         | Linux                                                           |
| Architecture   | x86_64                                                          |
| Processor      | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz                         |
| Model          | HP ProDesk 600 G5 SFF                                           |
| Logical Cores  | 8                                                               |
| Physical Cores | 8                                                               |
| Python         | 3.12.10                                                         |
| Torch          | 2.10.0+cpu                                                      |
| RAM Total (GB) | 33.4                                                            |
| BLAS           | blas 3.9.0                                                      |
| LAPACK         | lapack 3.9.0                                                    |

| Category        | Total Time (s) |
| --------------- | --------------:|
| Single Threaded | 91.43          |
| Parallel        | 378.49         |
| Memory Bound    | 26.96          |
| Compute Bound   | 553.12         |
| **Overall**     | **1,050.00**   |

### Single Threaded

| Benchmark              | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| ---------------------- | ------ | --------:| -------------:| -----------:|
| structure-function     | ok     | 58.67    | 3.41          | 100         |
| spectral-psd           | ok     | 5.21     | 4.46          | 99          |
| box-counting-dimension | ok     | 16.13    | 1.36          | 100         |
| perimeter              | ok     | 6.54     | 1.27          | 98          |
| levy-noise             | ok     | 4.88     | 3.23          | 99          |

### Parallel

| Benchmark             | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --------------------- | ------ | --------:| -------------:| -----------:|
| fif-nd-torch          | ok     | 5.37     | 3.96          | 636         |
| correlation-dimension | ok     | 230.39   | 1.05          | 766         |
| direct-convolution-3d | ok     | 65.25    | 3.19          | 761         |
| matmul-numpy          | ok     | 25.75    | 5.44          | 773         |
| matmul-torch          | ok     | 17.69    | 5.47          | 782         |
| svd                   | ok     | 34.03    | 1.38          | 767         |

### Memory Bound

| Benchmark         | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| ----------------- | ------ | --------:| -------------:| -----------:|
| write-allocate    | ok     | 0.22     | 2.84          | 92          |
| array-copy        | ok     | 0.18     | 3.14          | 90          |
| transpose-copy-3d | ok     | 1.05     | 1.93          | 99          |
| float-sort        | ok     | 24.15    | 2.92          | 100         |
| boolean-mask      | ok     | 1.37     | 2.54          | 98          |

### Compute Bound

| Benchmark       | Status | Time (s) | Peak Mem (GB) | Avg CPU (%) |
| --------------- | ------ | --------:| -------------:| -----------:|
| mandelbrot      | ok     | 67.98    | 0.65          | 294         |
| monte-carlo-pi  | ok     | 133.77   | 0.57          | 781         |
| transcendentals | ok     | 115.28   | 0.58          | 793         |
| n-body          | ok     | 144.99   | 0.60          | 784         |
| eigh            | ok     | 91.11    | 4.80          | 755         |

Result File: `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json`

</details>
