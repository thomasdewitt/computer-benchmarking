# Benchmark Summary

*Generated: 2026-03-25T18:52:59*

This summary compares the latest saved run for each machine using total wall time.

## Time Summary

| Machine                                                    | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run                       | Result File                                                                       |
| ---------------------------------------------------------- | -----------:| -------------------:| ------------:| ----------------:| -----------------:| -------------------------------- | --------------------------------------------------------------------------------- |
| Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 | 980.07      | 353.67              | 145.88       | 43.39            | 437.14            | 2026-03-26T00:17:56.850350+00:00 | `intel-r-xeon-r-cpu-e5-2680-v4-2-40ghz-poweredge-r430_fixed_20260325_183706.json` |
| Apple M1 / MacBook Air                                     | 1,069.64    | 84.09               | 454.23       | 32.79            | 498.52            | 2026-03-25T23:30:43.338605+00:00 | `apple-m1-macbook-air_fixed_20260325_174912.json`                                 |

## Benchmark Matrix

Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.

| Benchmark              | Workflow Type   | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 | Apple M1 / MacBook Air |
| ---------------------- | --------------- | ----------------------------------------------------------:| ----------------------:|
| structure-function     | Single Threaded | 277.88                                                     | 57.92                  |
| spectral-psd           | Single Threaded | 14.98                                                      | 5.69                   |
| box-counting-dimension | Single Threaded | 35.51                                                      | 10.45                  |
| perimeter              | Single Threaded | 10.18                                                      | 6.20                   |
| levy-noise             | Single Threaded | 15.10                                                      | 3.83                   |
| fif-nd-torch           | Parallel        | 11.43                                                      | 7.13                   |
| correlation-dimension  | Parallel        | 58.79                                                      | 269.36                 |
| direct-convolution-3d  | Parallel        | 22.42                                                      | 64.20                  |
| matmul-numpy           | Parallel        | 10.04                                                      | 41.75                  |
| matmul-torch           | Parallel        | 7.31                                                       | 36.09                  |
| svd                    | Parallel        | 35.89                                                      | 35.69                  |
| write-allocate         | Memory Bound    | 1.44                                                       | 0.19                   |
| array-copy             | Memory Bound    | 1.10                                                       | 0.15                   |
| transpose-copy-3d      | Memory Bound    | 2.60                                                       | 0.84                   |
| float-sort             | Memory Bound    | 35.94                                                      | 30.10                  |
| boolean-mask           | Memory Bound    | 2.29                                                       | 1.50                   |
| mandelbrot             | Compute Bound   | 15.30                                                      | 94.66                  |
| monte-carlo-pi         | Compute Bound   | 66.11                                                      | 99.95                  |
| transcendentals        | Compute Bound   | 228.13                                                     | 109.61                 |
| n-body                 | Compute Bound   | 41.75                                                      | 117.28                 |
| eigh                   | Compute Bound   | 85.84                                                      | 77.03                  |