from __future__ import annotations

import numpy as np
import torch

from .algorithms import (
    convolve_periodic_xy_zeropad_z,
    correlation_dimension,
    fif_nd_torch,
    make_multiscale_field,
)
from .harness import BenchmarkSpec


FIF_SHAPE = (8192, 8192)
ANALYSIS_SHAPE = (4096, 4096)
CORR_PRF = 10.0
CONV_SHAPE = (768, 768, 384)
KERNEL_SHAPE = (15, 15, 5)
MATMUL_SIZE = 14_336
SVD_SHAPE = (10_240, 5120)


def _fif_shape(system_info: dict | None) -> tuple[int, int]:
    return FIF_SHAPE


def _setup_matmul_state(state: dict[str, np.ndarray | torch.Tensor], size: int) -> None:
    rng_a = np.random.default_rng(43)
    rng_b = np.random.default_rng(44)
    mat_a = rng_a.standard_normal((size, size)).astype(np.float64)
    mat_b = rng_b.standard_normal((size, size)).astype(np.float64)
    state.update(
        {
            "mat_a": mat_a,
            "mat_b": mat_b,
            "torch_a": torch.from_numpy(mat_a),
            "torch_b": torch.from_numpy(mat_b),
        }
    )


def get_benchmarks(system_info: dict | None = None) -> list[BenchmarkSpec]:
    fif_shape = _fif_shape(system_info)
    analysis_shape = ANALYSIS_SHAPE
    conv_shape = CONV_SHAPE
    kernel_shape = KERNEL_SHAPE
    matmul_size = MATMUL_SIZE
    svd_shape = SVD_SHAPE
    fif_state: dict[str, torch.Tensor] = {}
    corr_state: dict[str, np.ndarray] = {}
    conv_state: dict[str, np.ndarray] = {}
    matmul_state: dict[str, np.ndarray | torch.Tensor] = {}
    svd_state: dict[str, np.ndarray] = {}

    def run_fif_torch():
        field = fif_nd_torch(fif_shape, alpha=2.0, c1=0.1, h=0.3, seed=43)
        field_np = field.detach().cpu().numpy()
        return {
            "mean": float(field_np.mean()),
            "std": float(field_np.std()),
            "finite_fraction": float(np.isfinite(field_np).mean()),
        }

    corr_prf = CORR_PRF

    def run_correlation_dimension():
        return correlation_dimension(
            corr_state["binary"],
            point_reduction_factor=corr_prf,
            nbins=40,
            seed=44,
        )

    def run_direct_convolution():
        out = convolve_periodic_xy_zeropad_z(conv_state["field"], conv_state["kernel"])
        return {"mean": float(out.mean()), "std": float(out.std())}

    def run_matmul_numpy():
        out = matmul_state["mat_a"] @ matmul_state["mat_b"]
        return {"frobenius_norm": float(np.linalg.norm(out)), "size": matmul_size}

    def run_matmul_torch():
        out = matmul_state["torch_a"] @ matmul_state["torch_b"]
        return {"frobenius_norm": float(torch.linalg.norm(out).item()), "size": matmul_size}

    def run_svd():
        singular_values = np.linalg.svd(
            svd_state["matrix"],
            full_matrices=False,
            compute_uv=False,
        )
        return {
            "largest_singular_value": float(singular_values[0]),
            "smallest_singular_value": float(singular_values[-1]),
        }

    return [
        BenchmarkSpec(
            category="parallel",
            name="fif-nd-torch",
            description="FFT-based 2D FIF cascade using local torch CPU implementation.",
            runner=run_fif_torch,
            metadata={"shape": fif_shape, "alpha": 2.0, "C1": 0.1, "H": 0.3},
            teardown=fif_state.clear,
        ),
        BenchmarkSpec(
            category="parallel",
            name="correlation-dimension",
            description="Boundary-point correlation integral with Numba prange and binary-search binning.",
            runner=run_correlation_dimension,
            metadata={"shape": analysis_shape, "point_reduction_factor": corr_prf},
            setup=lambda: corr_state.update(
                {
                    "binary": (
                        make_multiscale_field(analysis_shape, seed=42)
                        > 0.0
                    ).astype(np.uint8)
                }
            ),
            warmup=lambda: correlation_dimension(
                np.pad(np.ones((8, 8), dtype=np.uint8), 4),
                point_reduction_factor=1.0,
                nbins=8,
                seed=1,
            ),
            teardown=corr_state.clear,
        ),
        BenchmarkSpec(
            category="parallel",
            name="direct-convolution-3d",
            description="3D direct convolution with periodic x/y and zero-padded z.",
            runner=run_direct_convolution,
            metadata={"field_shape": conv_shape, "kernel_shape": kernel_shape},
            setup=lambda: conv_state.update(
                {
                    "field": np.random.default_rng(41).standard_normal(conv_shape).astype(np.float32),
                    "kernel": np.random.default_rng(42).standard_normal(kernel_shape).astype(np.float32),
                }
            ),
            warmup=lambda: convolve_periodic_xy_zeropad_z(
                np.zeros((8, 8, 8), dtype=np.float32),
                np.zeros((3, 3, 3), dtype=np.float32),
            ),
            teardown=conv_state.clear,
        ),
        BenchmarkSpec(
            category="parallel",
            name="matmul-numpy",
            description="Large BLAS-backed numpy dense matrix multiply.",
            runner=run_matmul_numpy,
            metadata={"size": matmul_size},
            setup=lambda: _setup_matmul_state(matmul_state, matmul_size),
            teardown=matmul_state.clear,
        ),
        BenchmarkSpec(
            category="parallel",
            name="matmul-torch",
            description="Large torch CPU dense matrix multiply.",
            runner=run_matmul_torch,
            metadata={"size": matmul_size},
            setup=lambda: _setup_matmul_state(matmul_state, matmul_size),
            teardown=matmul_state.clear,
        ),
        BenchmarkSpec(
            category="parallel",
            name="svd",
            description="Dense singular value decomposition using LAPACK.",
            runner=run_svd,
            metadata={"shape": svd_shape},
            setup=lambda: svd_state.update(
                {
                    "matrix": np.random.default_rng(45).standard_normal(svd_shape).astype(np.float64)
                }
            ),
            teardown=svd_state.clear,
        ),
    ]
