from __future__ import annotations

import numpy as np

from .algorithms import (
    box_counting_dimension,
    extremal_levy_numpy,
    fit_loglog,
    make_binary_field,
    make_multiscale_series,
    spectral_analysis,
    structure_function_analysis,
    total_perimeter_serial,
)
from .harness import BenchmarkSpec


PROFILE_STRUCTURE_LENGTH = {
    "quick": 18_000_000,
    "default": 2**22,
    "full": 180_000_000,
}

PROFILE_SPECTRAL_LENGTH = {
    "quick": 160_000_000,
    "default": 2**25,
    "full": 256_000_000,
}

PROFILE_BOX_SHAPE = {
    "quick": (7680, 7680),
    "default": (6144, 6144),
    "full": (12_288, 12_288),
}

PROFILE_PERIMETER_SHAPE = {
    "quick": (32_768, 32_768),
    "default": (20_000, 20_000),
    "full": (40_960, 40_960),
}

PROFILE_LEVY_SAMPLES = {
    "quick": 80_000_000,
    "default": 30_000_000,
    "full": 100_000_000,
}


def get_benchmarks(profile: str, system_info: dict | None = None) -> list[BenchmarkSpec]:
    structure_length = PROFILE_STRUCTURE_LENGTH[profile]
    spectral_length = PROFILE_SPECTRAL_LENGTH[profile]
    box_shape = PROFILE_BOX_SHAPE[profile]
    perimeter_shape = PROFILE_PERIMETER_SHAPE[profile]
    levy_samples = PROFILE_LEVY_SAMPLES[profile]
    structure_state: dict[str, np.ndarray] = {}
    spectral_state: dict[str, np.ndarray] = {}
    box_state: dict[str, np.ndarray] = {}
    perimeter_state: dict[str, np.ndarray] = {}

    def run_structure_function():
        lags, values = structure_function_analysis(
            structure_state["series"],
            order=1,
            max_sep=structure_length // 4,
            lags="powers of 1.15",
        )
        fit = fit_loglog(lags, values, min_x=4, max_x=structure_length // 8)
        return {
            "hurst_estimate": fit["slope"],
            "hurst_error": fit["slope_error"],
            "n_lags": int(len(lags)),
        }

    def run_spectral_analysis():
        freqs, psd = spectral_analysis(
            spectral_state["series"],
            max_wavelength=spectral_length / 8,
            min_wavelength=4,
            nbins=48,
            axis=0,
        )
        fit = fit_loglog(freqs, psd)
        hurst = ((-fit["slope"]) - 1.0) / 2.0
        return {
            "hurst_estimate": hurst,
            "hurst_error": fit["slope_error"] / 2.0,
            "n_bins": int(len(freqs)),
        }

    def run_box_counting():
        return box_counting_dimension(box_state["binary"])

    def run_perimeter():
        perimeter = total_perimeter_serial(
            perimeter_state["binary"],
            perimeter_state["x_sizes"],
            perimeter_state["y_sizes"],
        )
        return {
            "perimeter": float(perimeter),
            "coverage": float(perimeter_state["binary"].mean()),
        }

    def run_levy():
        noise = extremal_levy_numpy(1.8, levy_samples, seed=12)
        return {
            "mean": float(np.mean(noise)),
            "std": float(np.std(noise)),
            "q95_abs": float(np.quantile(np.abs(noise), 0.95)),
        }

    return [
        BenchmarkSpec(
            category="single_threaded",
            name="structure-function",
            description="First-order structure function with log-spaced lags and log-log fit.",
            runner=run_structure_function,
            threads=1,
            metadata={"length": structure_length},
            setup=lambda: structure_state.setdefault(
                "series",
                make_multiscale_series(structure_length, seed=10),
            ),
            teardown=structure_state.clear,
        ),
        BenchmarkSpec(
            category="single_threaded",
            name="spectral-psd",
            description="One-sided FFT power spectrum with logarithmic binning and slope fit.",
            runner=run_spectral_analysis,
            threads=1,
            metadata={"length": spectral_length},
            setup=lambda: spectral_state.setdefault(
                "series",
                make_multiscale_series(spectral_length, seed=11),
            ),
            teardown=spectral_state.clear,
        ),
        BenchmarkSpec(
            category="single_threaded",
            name="box-counting-dimension",
            description="Dyadic coarsening via numpy.add.reduceat for edge-set box counting.",
            runner=run_box_counting,
            threads=1,
            metadata={"shape": box_shape},
            setup=lambda: box_state.setdefault(
                "binary",
                make_binary_field(box_shape, seed=12),
            ),
            teardown=box_state.clear,
        ),
        BenchmarkSpec(
            category="single_threaded",
            name="perimeter",
            description="Serial Numba edge-counting perimeter with periodic boundaries.",
            runner=run_perimeter,
            threads=1,
            metadata={"shape": perimeter_shape},
            setup=lambda: perimeter_state.update(
                {
                    "binary": np.random.default_rng(13).integers(
                        0,
                        2,
                        size=perimeter_shape,
                        dtype=np.uint8,
                    ),
                    "x_sizes": np.broadcast_to(np.float32(1.0), perimeter_shape),
                    "y_sizes": np.broadcast_to(np.float32(1.0), perimeter_shape),
                }
            ),
            warmup=lambda: total_perimeter_serial(
                np.zeros((8, 8), dtype=np.uint8),
                np.ones((8, 8), dtype=np.float32),
                np.ones((8, 8), dtype=np.float32),
            ),
            teardown=perimeter_state.clear,
        ),
        BenchmarkSpec(
            category="single_threaded",
            name="levy-noise",
            description="Chambers-Mallows-Stuck extremal Levy noise generation.",
            runner=run_levy,
            threads=1,
            metadata={"samples": levy_samples, "alpha": 1.8},
        ),
    ]
