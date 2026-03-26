# Benchmark Summary

*Generated: 2026-03-26T11:49:45*

This summary compares the latest saved run for each machine using total wall time.

## Time Summary

| Machine                                                         | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run                       | Result File                                                                            |
| --------------------------------------------------------------- | -----------:| -------------------:| ------------:| ----------------:| -----------------:| -------------------------------- | -------------------------------------------------------------------------------------- |
| Apple M1 / MacBook Air                                          | 1,048.01    | 85.49               | 439.66       | 32.79            | 490.07            | 2026-03-26T17:31:33.744798+00:00 | `apple-m1-macbook-air_fixed_20260326_114945.json`                                      |
| Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | 1,050.00    | 91.43               | 378.49       | 26.96            | 553.12            | 2026-03-26T16:01:15.379316+00:00 | `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json` |

## Benchmark Matrix

Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.

| Benchmark              | Workflow Type   | Apple M1 / MacBook Air | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF |
| ---------------------- | --------------- | ----------------------:| ---------------------------------------------------------------:|
| structure-function     | Single Threaded | 57.78                  | 58.67                                                           |
| spectral-psd           | Single Threaded | 6.62                   | 5.21                                                            |
| box-counting-dimension | Single Threaded | 10.75                  | 16.13                                                           |
| perimeter              | Single Threaded | 6.41                   | 6.54                                                            |
| levy-noise             | Single Threaded | 3.94                   | 4.88                                                            |
| fif-nd-torch           | Parallel        | 7.47                   | 5.37                                                            |
| correlation-dimension  | Parallel        | 266.51                 | 230.39                                                          |
| direct-convolution-3d  | Parallel        | 55.05                  | 65.25                                                           |
| matmul-numpy           | Parallel        | 36.46                  | 25.75                                                           |
| matmul-torch           | Parallel        | 36.49                  | 17.69                                                           |
| svd                    | Parallel        | 37.67                  | 34.03                                                           |
| write-allocate         | Memory Bound    | 0.23                   | 0.22                                                            |
| array-copy             | Memory Bound    | 0.16                   | 0.18                                                            |
| transpose-copy-3d      | Memory Bound    | 0.84                   | 1.05                                                            |
| float-sort             | Memory Bound    | 30.06                  | 24.15                                                           |
| boolean-mask           | Memory Bound    | 1.49                   | 1.37                                                            |
| mandelbrot             | Compute Bound   | 94.49                  | 67.98                                                           |
| monte-carlo-pi         | Compute Bound   | 99.06                  | 133.77                                                          |
| transcendentals        | Compute Bound   | 106.96                 | 115.28                                                          |
| n-body                 | Compute Bound   | 115.21                 | 144.99                                                          |
| eigh                   | Compute Bound   | 74.35                  | 91.11                                                           |