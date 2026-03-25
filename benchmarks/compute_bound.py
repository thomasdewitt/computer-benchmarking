from __future__ import annotations

import math

import numba
import numpy as np

from .harness import BenchmarkSpec


MANDELBROT = (4608, 4608, 20_000)
MONTE_CARLO_SAMPLES = 600_000_000_000
TRANS_SIZE = (1_048_576, 20_000)
NBODY_PARTICLES = 425_984
EIGH_SIZE = 10_240


def _symmetric_matrix(size: int) -> np.ndarray:
    rng = np.random.default_rng(34)
    matrix = rng.standard_normal((size, size)).astype(np.float64)
    return 0.5 * (matrix + matrix.T)


@numba.njit(parallel=True, cache=True)
def mandelbrot_counts(width: int, height: int, max_iter: int) -> np.ndarray:
    out = np.empty((height, width), dtype=np.int32)
    for iy in numba.prange(height):
        cy = -1.5 + 3.0 * iy / max(1, height - 1)
        for ix in range(width):
            cx = -2.2 + 3.2 * ix / max(1, width - 1)
            zx = 0.0
            zy = 0.0
            count = 0
            while zx * zx + zy * zy <= 4.0 and count < max_iter:
                new_zx = zx * zx - zy * zy + cx
                zy = 2.0 * zx * zy + cy
                zx = new_zx
                count += 1
            out[iy, ix] = count
    return out


@numba.njit(parallel=True, cache=True)
def monte_carlo_pi_hits(num_samples: int, seed: int) -> int:
    inside = 0
    for i in numba.prange(num_samples):
        a = np.uint64(seed + i * 747796405)
        b = np.uint64(seed * 3 + i * 2891336453)
        x = ((a ^ (a >> np.uint64(16))) & np.uint64(0xFFFFFFFF)) / 4294967295.0
        y = ((b ^ (b >> np.uint64(16))) & np.uint64(0xFFFFFFFF)) / 4294967295.0
        if x * x + y * y <= 1.0:
            inside += 1
    return inside


@numba.njit(parallel=True, cache=True)
def transcendental_kernel(values: np.ndarray, repeats: int) -> float:
    buffer = values.copy()
    for repeat in range(repeats):
        for i in numba.prange(buffer.size):
            x = buffer[i] + repeat * 1e-6
            buffer[i] = (
                math.sin(x)
                + math.cos(1.7 * x)
                + math.exp(-0.2 * abs(x))
                + math.log1p(x * x)
            )
    return np.sum(buffer)


@numba.njit(parallel=True, cache=True)
def nbody_acceleration(positions: np.ndarray, masses: np.ndarray, softening: float) -> np.ndarray:
    n_particles = positions.shape[0]
    acceleration = np.zeros_like(positions)
    for i in numba.prange(n_particles):
        ax = 0.0
        ay = 0.0
        az = 0.0
        px = positions[i, 0]
        py = positions[i, 1]
        pz = positions[i, 2]
        for j in range(n_particles):
            if i == j:
                continue
            dx = positions[j, 0] - px
            dy = positions[j, 1] - py
            dz = positions[j, 2] - pz
            dist_sq = dx * dx + dy * dy + dz * dz + softening
            inv = 1.0 / math.sqrt(dist_sq)
            inv3 = masses[j] * inv * inv * inv
            ax += dx * inv3
            ay += dy * inv3
            az += dz * inv3
        acceleration[i, 0] = ax
        acceleration[i, 1] = ay
        acceleration[i, 2] = az
    return acceleration


def get_benchmarks(system_info: dict | None = None) -> list[BenchmarkSpec]:
    width, height, max_iter = MANDELBROT
    monte_carlo_samples = MONTE_CARLO_SAMPLES
    trans_size, trans_repeats = TRANS_SIZE
    n_particles = NBODY_PARTICLES
    eigh_size = EIGH_SIZE
    trans_state: dict[str, np.ndarray] = {}
    nbody_state: dict[str, np.ndarray] = {}
    eigh_state: dict[str, np.ndarray] = {}

    def run_mandelbrot():
        image = mandelbrot_counts(width, height, max_iter)
        return {
            "shape": [height, width],
            "escape_mean": float(image.mean()),
            "escape_max": int(image.max()),
        }

    def run_monte_carlo():
        inside_total = monte_carlo_pi_hits(monte_carlo_samples, 12345)
        estimate = 4.0 * inside_total / monte_carlo_samples
        return {
            "pi_estimate": float(estimate),
            "samples": monte_carlo_samples,
        }

    def run_transcendentals():
        total = transcendental_kernel(trans_state["values"], trans_repeats)
        return {"checksum": float(total), "elements": trans_size, "repeats": trans_repeats}

    def run_nbody():
        acceleration = nbody_acceleration(
            nbody_state["positions"],
            nbody_state["masses"],
            softening=1e-3,
        )
        norms = np.linalg.norm(acceleration, axis=1)
        return {
            "mean_acceleration": float(np.mean(norms)),
            "max_acceleration": float(np.max(norms)),
            "particles": n_particles,
        }

    def run_eigh():
        eigenvalues = np.linalg.eigh(eigh_state["matrix"])[0]
        return {
            "min_eigenvalue": float(eigenvalues[0]),
            "max_eigenvalue": float(eigenvalues[-1]),
            "size": eigh_size,
        }

    return [
        BenchmarkSpec(
            category="compute_bound",
            name="mandelbrot",
            description="Parallel Mandelbrot escape-time iteration over a dense pixel grid.",
            runner=run_mandelbrot,
            metadata={"width": width, "height": height, "max_iter": max_iter},
            warmup=lambda: mandelbrot_counts(16, 16, 10),
        ),
        BenchmarkSpec(
            category="compute_bound",
            name="monte-carlo-pi",
            description="Parallel pseudo-random point-in-circle test without large memory traffic.",
            runner=run_monte_carlo,
            metadata={"samples": monte_carlo_samples},
            warmup=lambda: monte_carlo_pi_hits(10_000, 1),
        ),
        BenchmarkSpec(
            category="compute_bound",
            name="transcendentals",
            description="Tight repeated sin/cos/exp/log1p loop over a cache-resident vector.",
            runner=run_transcendentals,
            metadata={"elements": trans_size, "repeats": trans_repeats},
            setup=lambda: trans_state.update(
                {
                    "values": np.random.default_rng(31).standard_normal(trans_size).astype(np.float64)
                }
            ),
            warmup=lambda: transcendental_kernel(np.linspace(-1.0, 1.0, 128), 2),
            teardown=trans_state.clear,
        ),
        BenchmarkSpec(
            category="compute_bound",
            name="n-body",
            description="All-pairs N-body force accumulation with O(N^2) arithmetic intensity.",
            runner=run_nbody,
            metadata={"particles": n_particles},
            setup=lambda: nbody_state.update(
                {
                    "positions": np.random.default_rng(32).standard_normal((n_particles, 3)).astype(np.float64),
                    "masses": np.abs(
                        np.random.default_rng(33).standard_normal(n_particles)
                    ).astype(np.float64)
                    + 0.1,
                }
            ),
            warmup=lambda: nbody_acceleration(
                np.zeros((8, 3), dtype=np.float64),
                np.ones(8, dtype=np.float64),
                1e-3,
            ),
            teardown=nbody_state.clear,
        ),
        BenchmarkSpec(
            category="compute_bound",
            name="eigh",
            description="Symmetric dense eigenvalue decomposition using LAPACK.",
            runner=run_eigh,
            metadata={"size": eigh_size},
            setup=lambda: eigh_state.update(
                {
                    "matrix": _symmetric_matrix(eigh_size)
                }
            ),
            teardown=eigh_state.clear,
        ),
    ]
