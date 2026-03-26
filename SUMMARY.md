# Benchmark Summary

*Generated: 2026-03-26T11:55:21*

This summary compares the latest saved run for each machine using total wall time.

## Time Summary

| Machine                                                         | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run                       | Result File                                                                            |
| --------------------------------------------------------------- | -----------:| -------------------:| ------------:| ----------------:| -----------------:| -------------------------------- | -------------------------------------------------------------------------------------- |
| Apple M1 / MacBook Air                                          | 1,048.01    | 85.49               | 439.66       | 32.79            | 490.07            | 2026-03-26T17:31:33.744798+00:00 | `apple-m1-macbook-air_fixed_20260326_114945.json`                                      |
| Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | 1,050.00    | 91.43               | 378.49       | 26.96            | 553.12            | 2026-03-26T16:01:15.379316+00:00 | `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json` |
| Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430      | 1,107.54    | 368.86              | 161.67       | 43.80            | 533.21            | 2026-03-26T17:31:04.562696+00:00 | `intel-r-xeon-r-cpu-e5-2680-v4-2-40ghz-poweredge-r430_fixed_20260326_115301.json`      |

## Benchmark Matrix

Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.

| Benchmark              | Workflow Type   | Apple M1 / MacBook Air | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 |
| ---------------------- | --------------- | ----------------------:| ---------------------------------------------------------------:| ----------------------------------------------------------:|
| structure-function     | Single Threaded | 57.78                  | 58.67                                                           | 290.49                                                     |
| spectral-psd           | Single Threaded | 6.62                   | 5.21                                                            | 15.37                                                      |
| box-counting-dimension | Single Threaded | 10.75                  | 16.13                                                           | 35.85                                                      |
| perimeter              | Single Threaded | 6.41                   | 6.54                                                            | 10.36                                                      |
| levy-noise             | Single Threaded | 3.94                   | 4.88                                                            | 16.78                                                      |
| fif-nd-torch           | Parallel        | 7.47                   | 5.37                                                            | 10.57                                                      |
| correlation-dimension  | Parallel        | 266.51                 | 230.39                                                          | 61.95                                                      |
| direct-convolution-3d  | Parallel        | 55.05                  | 65.25                                                           | 24.14                                                      |
| matmul-numpy           | Parallel        | 36.46                  | 25.75                                                           | 11.86                                                      |
| matmul-torch           | Parallel        | 36.49                  | 17.69                                                           | 8.18                                                       |
| svd                    | Parallel        | 37.67                  | 34.03                                                           | 44.98                                                      |
| write-allocate         | Memory Bound    | 0.23                   | 0.22                                                            | 1.36                                                       |
| array-copy             | Memory Bound    | 0.16                   | 0.18                                                            | 1.21                                                       |
| transpose-copy-3d      | Memory Bound    | 0.84                   | 1.05                                                            | 2.52                                                       |
| float-sort             | Memory Bound    | 30.06                  | 24.15                                                           | 36.21                                                      |
| boolean-mask           | Memory Bound    | 1.49                   | 1.37                                                            | 2.50                                                       |
| mandelbrot             | Compute Bound   | 94.49                  | 67.98                                                           | 15.94                                                      |
| monte-carlo-pi         | Compute Bound   | 99.06                  | 133.77                                                          | 68.68                                                      |
| transcendentals        | Compute Bound   | 106.96                 | 115.28                                                          | 305.16                                                     |
| n-body                 | Compute Bound   | 115.21                 | 144.99                                                          | 43.95                                                      |
| eigh                   | Compute Bound   | 74.35                  | 91.11                                                           | 99.49                                                      |