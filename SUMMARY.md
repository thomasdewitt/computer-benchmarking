# Benchmark Summary

*Generated: 2026-04-10T23:11:03*

This summary compares the latest saved run for each machine using total wall time.

## Time Summary

| Machine | Overall (s) | Single Threaded (s) | Parallel (s) | Memory Bound (s) | Compute Bound (s) | Latest Run | Result File |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| AMD Ryzen 9 9950X 16-Core Processor / X870 EAGLE WIFI7 | 287.55 | 79.87 | 75.86 | 20.01 | 111.82 | 2026-04-11T04:44:20.633234+00:00 | `amd-ryzen-9-9950x-16-core-processor-x870-eagle-wifi7_fixed_20260410_224942.json` |
| Apple M1 / MacBook Air | 1,048.01 | 85.49 | 439.66 | 32.79 | 490.07 | 2026-03-26T17:31:33.744798+00:00 | `apple-m1-macbook-air_fixed_20260326_114945.json` |
| Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | 1,050.00 | 91.43 | 378.49 | 26.96 | 553.12 | 2026-03-26T16:01:15.379316+00:00 | `intel-r-core-tm-i7-9700-cpu-3-00ghz-hp-prodesk-600-g5-sff_fixed_20260326_101937.json` |
| Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 | 1,107.54 | 368.86 | 161.67 | 43.80 | 533.21 | 2026-03-26T17:31:04.562696+00:00 | `intel-r-xeon-r-cpu-e5-2680-v4-2-40ghz-poweredge-r430_fixed_20260326_115301.json` |

## Benchmark Matrix

Each row is one benchmark. Values are wall time in seconds for the latest saved run per machine.

| Benchmark | Workflow Type | AMD Ryzen 9 9950X 16-Core Processor / X870 EAGLE WIFI7 | Apple M1 / MacBook Air | Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz / HP ProDesk 600 G5 SFF | Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz / PowerEdge R430 |
| --- | --- | ---: | ---: | ---: | ---: |
| structure-function | Single Threaded | 27.34 | 57.78 | 58.67 | 290.49 |
| spectral-psd | Single Threaded | 2.42 | 6.62 | 5.21 | 15.37 |
| box-counting-dimension | Single Threaded | 43.32 | 10.75 | 16.13 | 35.85 |
| perimeter | Single Threaded | 4.38 | 6.41 | 6.54 | 10.36 |
| levy-noise | Single Threaded | 2.40 | 3.94 | 4.88 | 16.78 |
| fif-nd-torch | Parallel | 2.88 | 7.47 | 5.37 | 10.57 |
| correlation-dimension | Parallel | 41.65 | 266.51 | 230.39 | 61.95 |
| direct-convolution-3d | Parallel | 7.69 | 55.05 | 65.25 | 24.14 |
| matmul-numpy | Parallel | 3.57 | 36.46 | 25.75 | 11.86 |
| matmul-torch | Parallel | 5.72 | 36.49 | 17.69 | 8.18 |
| svd | Parallel | 14.36 | 37.67 | 34.03 | 44.98 |
| write-allocate | Memory Bound | 0.13 | 0.23 | 0.22 | 1.36 |
| array-copy | Memory Bound | 0.10 | 0.16 | 0.18 | 1.21 |
| transpose-copy-3d | Memory Bound | 0.20 | 0.84 | 1.05 | 2.52 |
| float-sort | Memory Bound | 18.64 | 30.06 | 24.15 | 36.21 |
| boolean-mask | Memory Bound | 0.95 | 1.49 | 1.37 | 2.50 |
| mandelbrot | Compute Bound | 11.57 | 94.49 | 67.98 | 15.94 |
| monte-carlo-pi | Compute Bound | 7.56 | 99.06 | 133.77 | 68.68 |
| transcendentals | Compute Bound | 27.60 | 106.96 | 115.28 | 305.16 |
| n-body | Compute Bound | 30.36 | 115.21 | 144.99 | 43.95 |
| eigh | Compute Bound | 34.72 | 74.35 | 91.11 | 99.49 |