from __future__ import annotations

import math
from typing import Iterable

import numba
import numpy as np
from scipy import signal
from scipy.ndimage import label
import torch


def process_lags(lags: str | Iterable[int] | np.ndarray, max_sep: int, even_only: bool = False) -> np.ndarray:
    if isinstance(lags, (list, tuple, np.ndarray)):
        values = np.asarray(lags, dtype=np.int64)
    elif isinstance(lags, str):
        if lags == "all":
            values = np.arange(1, max_sep + 1, dtype=np.int64)
        elif lags.startswith("powers of "):
            base = float(lags[10:])
            values = np.array(
                [int(base**n) for n in range(int(np.log(max_sep) / np.log(base)) + 1)],
                dtype=np.int64,
            )
        else:
            raise ValueError(f"Unsupported lag option: {lags}")
    else:
        raise ValueError("lags must be a string or array-like")

    values = np.unique(values)
    values = values[(values > 0) & (values <= max_sep)]
    if even_only:
        values = values[values % 2 == 0]
    return values


def fit_loglog(x: np.ndarray, y: np.ndarray, min_x: float | None = None, max_x: float | None = None) -> dict[str, float]:
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)

    mask = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if min_x is not None:
        mask &= x >= min_x
    if max_x is not None:
        mask &= x <= max_x
    x = x[mask]
    y = y[mask]
    if x.size < 2:
        raise ValueError("Need at least two positive points for log-log regression")

    coeffs, cov = np.polyfit(np.log(x), np.log(y), 1, cov=True)
    slope, intercept = coeffs
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "slope_error": float(np.sqrt(cov[0, 0])),
        "n_points": int(x.size),
    }


def structure_function_analysis(
    data: np.ndarray,
    order: int = 1,
    max_sep: int | None = None,
    axis: int = 0,
    lags: str | Iterable[int] | np.ndarray = "powers of 1.2",
) -> tuple[np.ndarray, np.ndarray]:
    data = np.asarray(data)
    if max_sep is None:
        max_sep = data.shape[axis] - 1
    lags_array = process_lags(lags, max_sep, even_only=False)
    values = np.empty(lags_array.size, dtype=np.float64)

    for idx, lag in enumerate(lags_array):
        slice1 = [slice(None)] * data.ndim
        slice2 = [slice(None)] * data.ndim
        slice1[axis] = slice(lag, None)
        slice2[axis] = slice(None, -lag)
        diff = np.abs(data[tuple(slice1)] - data[tuple(slice2)])
        values[idx] = np.nanmean(diff**order)

    return lags_array, values


def spectral_analysis(
    data: np.ndarray,
    max_wavelength: float | None = None,
    min_wavelength: float | None = None,
    nbins: int = 50,
    axis: int = 0,
) -> tuple[np.ndarray, np.ndarray]:
    data = np.asarray(data)
    n = data.shape[axis]
    fft_values = np.fft.rfft(data, axis=axis)
    psd = np.abs(fft_values) ** 2 / n
    avg_axes = tuple(i for i in range(data.ndim) if i != axis)
    if avg_axes:
        psd = np.mean(psd, axis=avg_axes)
    freqs = np.fft.rfftfreq(n, d=1.0)

    mask = freqs > 0
    if max_wavelength is not None:
        mask &= freqs >= 1.0 / max_wavelength
    if min_wavelength is not None:
        mask &= freqs <= 1.0 / min_wavelength

    freqs = freqs[mask]
    psd = psd[mask]
    bins = np.logspace(np.log10(freqs.min()), np.log10(freqs.max()), nbins + 1)

    binned_freq = []
    binned_psd = []
    for start, end in zip(bins[:-1], bins[1:]):
        in_bin = (freqs >= start) & (freqs < end)
        if np.any(in_bin):
            binned_freq.append(freqs[in_bin].mean())
            binned_psd.append(psd[in_bin].mean())

    return np.asarray(binned_freq), np.asarray(binned_psd)


def haar_fluctuation_analysis(
    data: np.ndarray,
    order: int = 1,
    max_sep: int | None = None,
    axis: int = 0,
    lags: str | Iterable[int] | np.ndarray = "powers of 1.2",
) -> tuple[np.ndarray, np.ndarray]:
    data = np.asarray(data)
    if max_sep is None:
        max_sep = data.shape[axis] - 1
    lags_array = process_lags(lags, max_sep, even_only=True)
    values = []

    for lag in lags_array:
        kernel = np.ones(lag, dtype=np.float64) / (lag / 2.0)
        kernel[: lag // 2] *= -1.0
        kernel_shape = [1] * data.ndim
        kernel_shape[axis] = lag
        kernel = kernel.reshape(kernel_shape)
        filtered = signal.convolve(data, kernel, mode="valid", method="auto")
        values.append(float(np.mean(np.abs(filtered) ** order)))

    return lags_array, np.asarray(values, dtype=np.float64)


def make_multiscale_series(length: int, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    series = np.zeros(length, dtype=np.float64)
    block = 4
    while block <= max(8, length // 8):
        coarse = rng.standard_normal((length + block - 1) // block)
        expanded = np.repeat(coarse, block)[:length]
        series += expanded / math.sqrt(block)
        block *= 2
    series += 0.15 * rng.standard_normal(length)
    series -= series.mean()
    series /= series.std()
    return series


def make_multiscale_field(shape: tuple[int, int], seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    field = np.zeros(shape, dtype=np.float64)
    block = 4
    while block <= max(8, min(shape) // 4):
        coarse_shape = tuple((dim + block - 1) // block for dim in shape)
        coarse = rng.standard_normal(coarse_shape)
        expanded = np.kron(coarse, np.ones((block, block), dtype=np.float64))
        field += expanded[: shape[0], : shape[1]] / math.sqrt(block)
        block *= 2
    field += 0.1 * rng.standard_normal(shape)
    field -= field.mean()
    field /= field.std()
    return field


def make_binary_field(shape: tuple[int, int], seed: int = 0) -> np.ndarray:
    field = make_multiscale_field(shape, seed=seed)
    return (field > np.median(field)).astype(np.uint8)


def extremal_levy_numpy(alpha: float, size: int | tuple[int, ...], seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    phi = (rng.random(size) - 0.5) * np.pi
    phi0 = -(np.pi / 2.0) * (1.0 - abs(1.0 - alpha)) / alpha
    r = rng.exponential(scale=1.0, size=size)
    eps = 1e-12
    cos_phi = np.cos(phi)
    cos_phi = np.where(np.abs(cos_phi) < eps, eps, cos_phi)
    abs_alpha = max(abs(alpha - 1.0), eps)
    denom = np.cos(phi - alpha * (phi - phi0))
    denom = np.where(denom < eps, eps, denom)
    r = np.where(r < eps, eps, r)
    sample = (
        np.sign(alpha - 1.0)
        * np.sin(alpha * (phi - phi0))
        * (cos_phi * abs_alpha) ** (-1.0 / alpha)
        * (denom / r) ** ((1.0 - alpha) / alpha)
    )
    return sample


def _apply_outer_scale_numpy(
    kernel: np.ndarray,
    distance: np.ndarray,
    outer_scale: float,
    width_factor: float = 2.0,
) -> np.ndarray:
    transition_width = outer_scale * width_factor
    lower_edge = outer_scale - transition_width / 2.0
    upper_edge = outer_scale + transition_width / 2.0
    normalized = np.clip((distance - lower_edge) / transition_width, 0.0, 1.0)
    window = 0.5 * (1.0 + np.cos(np.pi * normalized))
    return kernel * window


def _apply_ls2010_correction_numpy(
    distance: np.ndarray,
    exponent: float,
    norm_ratio_exponent: float,
    final_power: float | None,
) -> np.ndarray:
    if distance.ndim == 1:
        domain_size = float(distance.size)
    else:
        domain_size = float(min(distance.shape))

    ratio = 2.0
    cutoff_length = domain_size / 2.0
    cutoff_length2 = cutoff_length / ratio
    base_kernel = distance**exponent
    exp1 = np.exp(np.clip(-(distance / cutoff_length) ** 4, -200.0, 0.0))
    exp2 = np.exp(np.clip(-(distance / cutoff_length2) ** 4, -200.0, 0.0))
    norm1 = np.sum(base_kernel * exp1)
    norm2 = np.sum(base_kernel * exp2)
    ratio_factor = ratio**norm_ratio_exponent
    normalization = (ratio_factor * norm1 - norm2) / (ratio_factor - 1.0)
    final_filter = np.exp(np.clip(-distance / 3.0, -200.0, 0.0))
    filter_integral = np.sum(base_kernel * final_filter)
    correction_factor = -normalization / filter_integral
    corrected = base_kernel * (1.0 + correction_factor * final_filter)
    if final_power is not None:
        corrected = corrected**final_power
    return corrected


def create_kernel_ls2010_numpy(
    size: int | tuple[int, ...],
    exponent: float,
    norm_ratio_exponent: float,
    *,
    outer_scale: float | None = None,
    outer_scale_width_factor: float = 2.0,
    final_power: float | None = None,
) -> np.ndarray:
    if isinstance(size, int):
        coords = np.arange(-(size - 1), size, 2, dtype=np.float64)
        distance = np.abs(coords)
    else:
        coord_arrays = [np.arange(-(dim - 1), dim, 2, dtype=np.float64) for dim in size]
        coord_grids = np.meshgrid(*coord_arrays, indexing="ij")
        distance = np.sqrt(sum(grid**2 for grid in coord_grids))

    kernel = _apply_ls2010_correction_numpy(distance, exponent, norm_ratio_exponent, final_power)
    if outer_scale is not None:
        kernel = _apply_outer_scale_numpy(
            kernel,
            distance / 2.0,
            outer_scale,
            width_factor=outer_scale_width_factor,
        )
    return kernel


def periodic_convolve_nd_numpy(signal_array: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    shifted_kernel = np.fft.ifftshift(kernel)
    return np.real(np.fft.ifftn(np.fft.fftn(signal_array) * np.fft.fftn(shifted_kernel)))


def fif_nd_numpy(
    size: tuple[int, int],
    alpha: float,
    c1: float,
    h: float,
    *,
    seed: int = 0,
    outer_scale: float | None = None,
) -> np.ndarray:
    if outer_scale is None:
        outer_scale = float(max(size))

    noise = extremal_levy_numpy(alpha, size=size, seed=seed)
    ndim = float(len(size))
    alpha_prime = 1.0 / (1.0 - 1.0 / alpha)

    flux_kernel = create_kernel_ls2010_numpy(
        size,
        exponent=-ndim / alpha_prime,
        norm_ratio_exponent=-ndim / alpha,
        outer_scale=outer_scale,
        final_power=1.0 / (alpha - 1.0),
    )
    integrated = periodic_convolve_nd_numpy(noise, flux_kernel)
    flux = np.exp(integrated * (c1 ** (1.0 / alpha)))
    if h == 0:
        flux /= np.mean(flux)
        return flux

    observable_kernel = create_kernel_ls2010_numpy(
        size,
        exponent=-ndim + h,
        norm_ratio_exponent=-h,
        outer_scale=outer_scale,
        final_power=None,
    )
    observable = periodic_convolve_nd_numpy(flux, observable_kernel)
    observable /= np.mean(observable)
    return observable


def extremal_levy_torch(
    alpha: float,
    size: tuple[int, ...],
    *,
    seed: int = 0,
    dtype: torch.dtype = torch.float64,
    device: str = "cpu",
) -> torch.Tensor:
    generator = torch.Generator(device=device)
    generator.manual_seed(seed)
    phi = (torch.rand(size, generator=generator, dtype=dtype, device=device) - 0.5) * torch.pi
    phi0 = -(torch.pi / 2.0) * (1.0 - abs(1.0 - alpha)) / alpha
    u = torch.rand(size, generator=generator, dtype=dtype, device=device)
    r = -torch.log(torch.clamp(1.0 - u, min=1e-12))
    eps = torch.tensor(1e-12, dtype=dtype, device=device)
    cos_phi = torch.cos(phi)
    cos_phi = torch.where(torch.abs(cos_phi) < eps, eps, cos_phi)
    abs_alpha = max(abs(alpha - 1.0), 1e-12)
    denom = torch.cos(phi - alpha * (phi - phi0))
    denom = torch.where(denom < eps, eps, denom)
    return (
        math.copysign(1.0, alpha - 1.0)
        * torch.sin(alpha * (phi - phi0))
        * (cos_phi * abs_alpha) ** (-1.0 / alpha)
        * (denom / r) ** ((1.0 - alpha) / alpha)
    )


def _apply_outer_scale_torch(
    kernel: torch.Tensor,
    distance: torch.Tensor,
    outer_scale: float,
    width_factor: float = 2.0,
) -> torch.Tensor:
    transition_width = outer_scale * width_factor
    lower_edge = outer_scale - transition_width / 2.0
    normalized = torch.clamp((distance - lower_edge) / transition_width, 0.0, 1.0)
    window = 0.5 * (1.0 + torch.cos(torch.pi * normalized))
    return kernel * window


def _apply_ls2010_correction_torch(
    distance: torch.Tensor,
    exponent: float,
    norm_ratio_exponent: float,
    final_power: float | None,
) -> torch.Tensor:
    if distance.ndim == 1:
        domain_size = float(distance.shape[0])
    else:
        domain_size = float(min(distance.shape))

    ratio = 2.0
    cutoff_length = domain_size / 2.0
    cutoff_length2 = cutoff_length / ratio
    base_kernel = distance**exponent
    exp1 = torch.exp(torch.clamp(-(distance / cutoff_length) ** 4, min=-200.0, max=0.0))
    exp2 = torch.exp(torch.clamp(-(distance / cutoff_length2) ** 4, min=-200.0, max=0.0))
    norm1 = torch.sum(base_kernel * exp1)
    norm2 = torch.sum(base_kernel * exp2)
    ratio_factor = ratio**norm_ratio_exponent
    normalization = (ratio_factor * norm1 - norm2) / (ratio_factor - 1.0)
    final_filter = torch.exp(torch.clamp(-distance / 3.0, min=-200.0, max=0.0))
    filter_integral = torch.sum(base_kernel * final_filter)
    correction = -normalization / filter_integral
    corrected = base_kernel * (1.0 + correction * final_filter)
    if final_power is not None:
        corrected = corrected**final_power
    return corrected


def create_kernel_ls2010_torch(
    size: tuple[int, int],
    exponent: float,
    norm_ratio_exponent: float,
    *,
    outer_scale: float | None = None,
    outer_scale_width_factor: float = 2.0,
    final_power: float | None = None,
    dtype: torch.dtype = torch.float64,
    device: str = "cpu",
) -> torch.Tensor:
    coord_arrays = [
        torch.arange(-(dim - 1), dim, 2, dtype=dtype, device=device)
        for dim in size
    ]
    coord_grids = torch.meshgrid(*coord_arrays, indexing="ij")
    distance = torch.sqrt(sum(grid**2 for grid in coord_grids))
    kernel = _apply_ls2010_correction_torch(distance, exponent, norm_ratio_exponent, final_power)
    if outer_scale is not None:
        kernel = _apply_outer_scale_torch(
            kernel,
            distance / 2.0,
            outer_scale,
            width_factor=outer_scale_width_factor,
        )
    return kernel


def periodic_convolve_nd_torch(signal_array: torch.Tensor, kernel: torch.Tensor) -> torch.Tensor:
    shifted_kernel = torch.fft.ifftshift(kernel)
    return torch.real(torch.fft.ifftn(torch.fft.fftn(signal_array) * torch.fft.fftn(shifted_kernel)))


def fif_nd_torch(
    size: tuple[int, int],
    alpha: float,
    c1: float,
    h: float,
    *,
    seed: int = 0,
    outer_scale: float | None = None,
    dtype: torch.dtype = torch.float64,
) -> torch.Tensor:
    if outer_scale is None:
        outer_scale = float(max(size))

    noise = extremal_levy_torch(alpha, size, seed=seed, dtype=dtype)
    ndim = float(len(size))
    alpha_prime = 1.0 / (1.0 - 1.0 / alpha)
    flux_kernel = create_kernel_ls2010_torch(
        size,
        exponent=-ndim / alpha_prime,
        norm_ratio_exponent=-ndim / alpha,
        outer_scale=outer_scale,
        final_power=1.0 / (alpha - 1.0),
        dtype=dtype,
    )
    integrated = periodic_convolve_nd_torch(noise, flux_kernel)
    flux = torch.exp(integrated * (c1 ** (1.0 / alpha)))
    if h == 0:
        flux = flux / torch.mean(flux)
        return flux

    observable_kernel = create_kernel_ls2010_torch(
        size,
        exponent=-ndim + h,
        norm_ratio_exponent=-h,
        outer_scale=outer_scale,
        dtype=dtype,
    )
    observable = periodic_convolve_nd_torch(flux, observable_kernel)
    observable = observable / torch.mean(observable)
    return observable


def encase_in_value(array: np.ndarray, value: float = np.nan) -> np.ndarray:
    return np.pad(array, 1, constant_values=value)


def coarsen_array(array: np.ndarray, factor: int) -> np.ndarray:
    reduced = np.add.reduceat(array, np.arange(0, array.shape[0], factor), axis=0)
    reduced = np.add.reduceat(reduced, np.arange(0, array.shape[1], factor), axis=1)
    pixel_counts = np.add.reduceat(np.ones(array.shape), np.arange(0, array.shape[0], factor), axis=0)
    pixel_counts = np.add.reduceat(pixel_counts, np.arange(0, array.shape[1], factor), axis=1)
    return reduced / pixel_counts


def box_counting_dimension(
    binary_array: np.ndarray,
    *,
    set_type: str = "edge",
    min_pixels: int = 1,
    min_box_size: int = 2,
) -> dict[str, float]:
    box_sizes = 2 ** np.arange(1, 15)
    max_coarsening = min(binary_array.shape) / min_pixels
    box_sizes = box_sizes[(box_sizes <= max_coarsening) & (box_sizes >= min_box_size)]
    counts = []
    for factor in box_sizes:
        coarsened = encase_in_value(coarsen_array(binary_array, int(factor)), np.nan)
        if set_type == "edge":
            counts.append(np.count_nonzero((coarsened > 0) & (coarsened < 1)))
        else:
            counts.append(np.count_nonzero(coarsened > 0))
    counts = np.asarray(counts, dtype=np.float64)
    counts[counts == 0] = np.nan
    valid = np.isfinite(counts) & (counts > 0)
    coeffs, cov = np.polyfit(np.log10(box_sizes[valid]), np.log10(counts[valid]), 1, cov=True)
    return {
        "dimension": float(-coeffs[0]),
        "error": float(np.sqrt(cov[0, 0])),
        "n_box_sizes": int(valid.sum()),
    }


def get_boundary_coords(array: np.ndarray) -> np.ndarray:
    array = array.astype(np.int16)
    shifted_right = np.roll(array, shift=1, axis=1)
    shifted_down = np.roll(array, shift=1, axis=0)
    diff_right = shifted_right - array
    diff_down = shifted_down - array
    right_side = np.argwhere(diff_right == 1)
    right_side[:, 1] -= 1
    left_side = np.argwhere(diff_right == -1)
    bottom = np.argwhere(diff_down == 1)
    bottom[:, 0] -= 1
    top = np.argwhere(diff_down == -1)
    coords = np.vstack((right_side, left_side, bottom, top))
    return np.unique(coords, axis=0)


@numba.njit(parallel=True, cache=True)
def correlation_integral(centers_phys, sorted_boundary_phys, bins_sq, max_bin):
    sorted_y = sorted_boundary_phys[:, 1].copy()
    num_bins = bins_sq.shape[0]
    hist_per_thread = np.zeros((numba.config.NUMBA_NUM_THREADS, num_bins))

    for i in numba.prange(centers_phys.shape[0]):
        thread_id = numba.get_thread_id()
        cx = centers_phys[i, 0]
        cy = centers_phys[i, 1]
        lo = np.searchsorted(sorted_y, cy - max_bin, side="left")
        hi = np.searchsorted(sorted_y, cy + max_bin, side="right")

        for j in range(lo, hi):
            bx = sorted_boundary_phys[j, 0]
            if abs(bx - cx) > max_bin:
                continue
            dx = cx - bx
            dy = cy - sorted_boundary_phys[j, 1]
            dist_sq = dx * dx + dy * dy
            bin_idx = np.searchsorted(bins_sq, dist_sq, side="right")
            if bin_idx < num_bins:
                hist_per_thread[thread_id, bin_idx] += 1.0

    hist = np.sum(hist_per_thread, axis=0)
    counts = np.zeros(num_bins)
    cumulative = 0.0
    for idx in range(num_bins):
        cumulative += hist[idx]
        counts[idx] = cumulative
    return counts


def correlation_dimension(
    binary_array: np.ndarray,
    *,
    point_reduction_factor: float = 10.0,
    nbins: int = 40,
    seed: int = 0,
) -> dict[str, float]:
    boundary = get_boundary_coords(binary_array)
    if boundary.size == 0:
        raise ValueError("No boundary points available")

    height, width = binary_array.shape
    maxlength = 0.33 * min(height, width)
    minlength = 3.0
    bins = np.geomspace(minlength, maxlength, nbins)

    interior = boundary[
        (boundary[:, 0] >= maxlength)
        & (boundary[:, 0] < height - maxlength)
        & (boundary[:, 1] >= maxlength)
        & (boundary[:, 1] < width - maxlength)
    ]
    if interior.size == 0:
        interior = boundary

    if point_reduction_factor > 1:
        rng = np.random.default_rng(seed)
        count = max(1, int(len(interior) / point_reduction_factor))
        selection = rng.choice(len(interior), size=count, replace=False)
        interior = interior[selection]

    boundary_phys = boundary.astype(np.float64)
    centers_phys = interior.astype(np.float64)
    order = np.argsort(boundary_phys[:, 1])
    sorted_boundary = boundary_phys[order]
    counts = correlation_integral(centers_phys, sorted_boundary, bins**2, bins[-1])
    valid = np.isfinite(counts) & (counts > 0)
    coeffs, cov = np.polyfit(np.log10(bins[valid]), np.log10(counts[valid]), 1, cov=True)
    return {
        "dimension": float(coeffs[0]),
        "error": float(2.0 * np.sqrt(cov[0, 0])),
        "n_centers": int(len(centers_phys)),
        "coverage": float(binary_array.mean()),
    }


@numba.njit(cache=True)
def total_perimeter_serial(array, x_sizes, y_sizes):
    perimeter = 0.0
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            value = array[i, j]
            if value == 1:
                if i != array.shape[0] - 1 and array[i + 1, j] == 0:
                    perimeter += x_sizes[i, j]
                elif i == array.shape[0] - 1 and array[0, j] == 0:
                    perimeter += x_sizes[i, j]

                if i != 0 and array[i - 1, j] == 0:
                    perimeter += x_sizes[i, j]
                elif i == 0 and array[array.shape[0] - 1, j] == 0:
                    perimeter += x_sizes[i, j]

                if j != array.shape[1] - 1 and array[i, j + 1] == 0:
                    perimeter += y_sizes[i, j]
                elif j == array.shape[1] - 1 and array[i, 0] == 0:
                    perimeter += y_sizes[i, j]

                if j != 0 and array[i, j - 1] == 0:
                    perimeter += y_sizes[i, j]
                elif j == 0 and array[i, array.shape[1] - 1] == 0:
                    perimeter += y_sizes[i, j]
    return perimeter


@numba.njit(parallel=True, cache=True)
def convolve_periodic_xy_zeropad_z(field, kernel):
    nx, ny, nz = field.shape
    kx, ky, kz = kernel.shape
    half_kx = kx // 2
    half_ky = ky // 2
    half_kz = kz // 2

    result = np.empty((nx, ny, nz), dtype=np.float32)
    sx_lut = np.empty((nx, kx), dtype=np.int64)
    sy_lut = np.empty((ny, ky), dtype=np.int64)

    for ix in range(nx):
        for dkx in range(kx):
            sx_lut[ix, dkx] = (ix - dkx + half_kx) % nx

    for iy in range(ny):
        for dky in range(ky):
            sy_lut[iy, dky] = (iy - dky + half_ky) % ny

    for ix in numba.prange(nx):
        sx_row = sx_lut[ix]
        for iy in range(ny):
            sy_row = sy_lut[iy]
            for iz in range(nz):
                total = np.float64(0.0)
                for dkx in range(kx):
                    sx = sx_row[dkx]
                    for dky in range(ky):
                        sy = sy_row[dky]
                        for dkz in range(kz):
                            sz = iz - dkz + half_kz
                            if 0 <= sz < nz:
                                total += field[sx, sy, sz] * kernel[dkx, dky, dkz]
                result[ix, iy, iz] = np.float32(total)
    return result
