"""Linear reconstruction on a Cartesian grid clipped to the canister.

Linear interpolation inside the convex hull of the samples cannot invent a
hotter or colder value than the samples themselves. Nodes outside the hull
stay empty. The indicative uncertainty grows where the local samples disagree
and where the node is far from the nearest sample. It is a display model,
not a GUM uncertainty budget.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy.spatial import cKDTree

from dose3d_canister.geometry import CanisterGeometry, inside_canister
from dose3d_canister.io import DosePoints


@dataclass(frozen=True)
class DoseVolume:
    x_mm: np.ndarray
    y_mm: np.ndarray
    z_mm: np.ndarray
    dose_gy: np.ndarray
    indicative_uncertainty_gy: np.ndarray
    nearest_mm: np.ndarray
    density_per_cm3: np.ndarray
    inside: np.ndarray
    spacing_mm: tuple[float, float, float]
    method: str = "linear"


def reconstruct(
    points: DosePoints,
    geometry: CanisterGeometry,
    spacing_mm: float = 2.0,
    density_radius_mm: float = 15.0,
    neighbor_count: int = 4,
) -> DoseVolume:
    """Interpolate dose onto nodes that lie inside the canister and the hull."""

    if spacing_mm <= 0:
        raise ValueError("spacing_mm must be positive.")
    if density_radius_mm <= 0:
        raise ValueError("density_radius_mm must be positive.")
    _reject_points_outside(points, geometry)
    _reject_duplicates(points)
    _reject_flat_cloud(points)

    x_axis = _inclusive_axis(-geometry.inner_radius_mm, geometry.inner_radius_mm, spacing_mm)
    y_axis = _inclusive_axis(-geometry.inner_radius_mm, geometry.inner_radius_mm, spacing_mm)
    z_axis = _inclusive_axis(0.0, geometry.height_mm, spacing_mm)
    xx, yy, zz = np.meshgrid(x_axis, y_axis, z_axis, indexing="ij")
    inside = inside_canister(xx, yy, zz, geometry)

    interpolant = LinearNDInterpolator(points.xyz, points.dose_gy, fill_value=np.nan)
    dose = np.asarray(interpolant(np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])), dtype=float)
    dose = dose.reshape(xx.shape)
    dose = np.where(inside, dose, np.nan)

    grid = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])
    tree = cKDTree(points.xyz)
    nearest, uncertainty, density = _sample_support(
        tree,
        points,
        grid,
        neighbor_count=neighbor_count,
        density_radius_mm=density_radius_mm,
    )
    shape = xx.shape
    nearest = nearest.reshape(shape)
    uncertainty = uncertainty.reshape(shape)
    density = density.reshape(shape)
    hidden = ~inside
    nearest = np.where(hidden, np.nan, nearest)
    uncertainty = np.where(hidden | ~np.isfinite(dose), np.nan, uncertainty)
    density = np.where(hidden, np.nan, density)

    spacing = (
        float(x_axis[1] - x_axis[0]),
        float(y_axis[1] - y_axis[0]),
        float(z_axis[1] - z_axis[0]),
    )
    return DoseVolume(
        x_mm=x_axis,
        y_mm=y_axis,
        z_mm=z_axis,
        dose_gy=dose,
        indicative_uncertainty_gy=uncertainty,
        nearest_mm=nearest,
        density_per_cm3=density,
        inside=inside,
        spacing_mm=spacing,
    )


def dose_at(
    points: DosePoints,
    xyz_mm: tuple[float, float, float],
) -> float:
    """Linear interpolant at one coordinate. NaN when it falls outside the hull."""

    interpolant = LinearNDInterpolator(points.xyz, points.dose_gy, fill_value=np.nan)
    value = interpolant([xyz_mm])[0]
    return float(value)


def _inclusive_axis(start: float, stop: float, spacing: float) -> np.ndarray:
    steps = int(round((stop - start) / spacing))
    if steps < 1:
        raise ValueError("spacing_mm is larger than the canister.")
    return np.linspace(start, stop, steps + 1)


def _reject_points_outside(points: DosePoints, geometry: CanisterGeometry) -> None:
    mask = inside_canister(points.x_mm, points.y_mm, points.z_mm, geometry)
    if bool(mask.all()):
        return
    bad = np.flatnonzero(~mask)[:5]
    preview = ", ".join(
        f"({points.x_mm[i]:.3g}, {points.y_mm[i]:.3g}, {points.z_mm[i]:.3g})" for i in bad
    )
    raise ValueError(
        f"{int((~mask).sum())} points are outside the {geometry.name} canister. First: {preview}."
    )


def _reject_duplicates(points: DosePoints) -> None:
    rounded = np.round(points.xyz, decimals=6)
    _, counts = np.unique(rounded, axis=0, return_counts=True)
    if int(counts.max()) > 1:
        raise ValueError("Duplicate coordinates are not allowed.")


def _reject_flat_cloud(points: DosePoints) -> None:
    if len(points) < 4:
        raise ValueError("At least 4 non-coplanar points are required.")
    centered = points.xyz - points.xyz.mean(axis=0)
    rank = np.linalg.matrix_rank(centered, tol=1e-6)
    if int(rank) < 3:
        raise ValueError("Points are collinear or coplanar, so there is no 3D hull.")


def _sample_support(
    tree: cKDTree,
    points: DosePoints,
    grid: np.ndarray,
    neighbor_count: int,
    density_radius_mm: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    k_eff = min(max(neighbor_count, 1), len(points))
    distances, indices = tree.query(grid, k=k_eff)
    if k_eff == 1:
        distances = distances[:, None]
        indices = indices[:, None]
    nearest = distances[:, 0]
    neighbor_doses = points.dose_gy[indices]
    local_std = neighbor_doses.std(axis=1)

    sample_gap = tree.query(points.xyz, k=min(2, len(points)))[0]
    if sample_gap.ndim == 1:
        characteristic = float(np.median(sample_gap))
    else:
        characteristic = float(np.median(sample_gap[:, 1]))
    characteristic = max(characteristic, 1e-6)
    gap_term = local_std * (nearest / characteristic)

    if points.uncertainty_gy is None:
        uncertainty = gap_term
    else:
        weights = 1.0 / np.maximum(distances, 1e-6)
        weights /= weights.sum(axis=1, keepdims=True)
        measured = (weights * points.uncertainty_gy[indices]).sum(axis=1)
        uncertainty = np.hypot(measured, gap_term)

    counts = np.array([len(bucket) for bucket in tree.query_ball_point(grid, density_radius_mm)])
    volume_cm3 = (4.0 / 3.0) * np.pi * (density_radius_mm / 10.0) ** 3
    density = counts / volume_cm3
    return nearest, uncertainty, density
