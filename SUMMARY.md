# Benchmark Summary

*Generated: 2026-03-25T17:49:12*

This summary compares the latest saved run for each machine using total wall time.

## Time Summary

| Machine | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run | Result File |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Apple M1 / MacBook Air | 1,069.64 | 84.09 | 454.23 | 32.79 | 498.52 | 2026-03-25T23:30:43.338605+00:00 | `apple-m1-macbook-air_fixed_20260325_174912.json` |

## Benchmark Matrix

Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.

| Benchmark | Workflow Type | Apple M1 / MacBook Air |
| --- | --- | ---: |
| structure-function | Single Threaded | 57.92 |
| spectral-psd | Single Threaded | 5.69 |
| box-counting-dimension | Single Threaded | 10.45 |
| perimeter | Single Threaded | 6.20 |
| levy-noise | Single Threaded | 3.83 |
| fif-nd-torch | Parallel | 7.13 |
| correlation-dimension | Parallel | 269.36 |
| direct-convolution-3d | Parallel | 64.20 |
| matmul-numpy | Parallel | 41.75 |
| matmul-torch | Parallel | 36.09 |
| svd | Parallel | 35.69 |
| write-allocate | Memory Bound | 0.19 |
| array-copy | Memory Bound | 0.15 |
| transpose-copy-3d | Memory Bound | 0.84 |
| float-sort | Memory Bound | 30.10 |
| boolean-mask | Memory Bound | 1.50 |
| mandelbrot | Compute Bound | 94.66 |
| monte-carlo-pi | Compute Bound | 99.95 |
| transcendentals | Compute Bound | 109.61 |
| n-body | Compute Bound | 117.28 |
| eigh | Compute Bound | 77.03 |