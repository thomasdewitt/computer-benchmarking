# Benchmark Summary

*Generated: 2026-03-26T10:19:37*

This summary compares the latest saved run for each machine using total wall time.

## Time Summary

| Machine                                                         | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run                       | Result File                                                                            |
| --------------------------------------------------------------- | -----------:| -------------------:| ------------:| ----------------:| -----------------:| -------------------------------- | -------------------------------------------------------------------------------------- |
| Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | 1,050.00    | 91.43               | 378.49       | 26.96            | 553.12            | 2026-03-26T16:01:15.379316+00:00 | `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json` |

## Benchmark Matrix

Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.

| Benchmark              | Workflow Type   | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF |
| ---------------------- | --------------- | ---------------------------------------------------------------:|
| structure-function     | Single Threaded | 58.67                                                           |
| spectral-psd           | Single Threaded | 5.21                                                            |
| box-counting-dimension | Single Threaded | 16.13                                                           |
| perimeter              | Single Threaded | 6.54                                                            |
| levy-noise             | Single Threaded | 4.88                                                            |
| fif-nd-torch           | Parallel        | 5.37                                                            |
| correlation-dimension  | Parallel        | 230.39                                                          |
| direct-convolution-3d  | Parallel        | 65.25                                                           |
| matmul-numpy           | Parallel        | 25.75                                                           |
| matmul-torch           | Parallel        | 17.69                                                           |
| svd                    | Parallel        | 34.03                                                           |
| write-allocate         | Memory Bound    | 0.22                                                            |
| array-copy             | Memory Bound    | 0.18                                                            |
| transpose-copy-3d      | Memory Bound    | 1.05                                                            |
| float-sort             | Memory Bound    | 24.15                                                           |
| boolean-mask           | Memory Bound    | 1.37                                                            |
| mandelbrot             | Compute Bound   | 67.98                                                           |
| monte-carlo-pi         | Compute Bound   | 133.77                                                          |
| transcendentals        | Compute Bound   | 115.28                                                          |
| n-body                 | Compute Bound   | 144.99                                                          |
| eigh                   | Compute Bound   | 91.11                                                           |