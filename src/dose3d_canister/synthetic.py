"""Illustrative canister field for demos and tests.

The canister rotates between fixed Cs-137 sources, so a published isodose
map is roughly axisymmetric: higher toward the wall, lower toward the ends.
This generator copies that shape and pins the centre to 25 Gy. It is not a
measurement and not a Monte Carlo transport result.
"""

from __future__ import annotations

import numpy as np

from dose3d_canister.geometry import GAMMACELL_3000_ELAN, CanisterGeometry
from dose3d_canister.io import DosePoints

SYNTHETIC_NOTE = (
    "Illustrative axisymmetric field. Centre fixed at the requested dose, "
    "higher at the cylindrical wall and lower at the ends. Not a measurement."
)

# Wall / centre at mid-height, and the axial drop from mid-height to the end.
_WALL_GAIN = 0.28
_AXIAL_DROP = 0.12


def synthetic_dose_gy(
    x_mm: np.ndarray,
    y_mm: np.ndarray,
    z_mm: np.ndarray,
    geometry: CanisterGeometry = GAMMACELL_3000_ELAN,
    central_gy: float = 25.0,
) -> np.ndarray:
    radius_term = (np.square(x_mm) + np.square(y_mm)) / geometry.inner_radius_mm**2
    axial_term = np.square((z_mm - geometry.mid_height_mm) / geometry.mid_height_mm)
    return central_gy * (1.0 + _WALL_GAIN * radius_term) * (1.0 - _AXIAL_DROP * axial_term)


def sample_positions(
    geometry: CanisterGeometry = GAMMACELL_3000_ELAN,
    radial_mm: tuple[float, ...] = (0.0, 20.0, 40.0, 55.0, 61.0),
    n_angles: int = 12,
    z_mm: tuple[float, ...] = (2.0, 20.0, 50.0, 97.0, 144.0, 174.0, 192.0),
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cylindrical lattice that includes the axis and the central plane."""

    xs: list[float] = []
    ys: list[float] = []
    zs: list[float] = []
    angles = np.linspace(0.0, 2.0 * np.pi, n_angles, endpoint=False)
    for z in z_mm:
        for radius in radial_mm:
            if radius == 0.0:
                xs.append(0.0)
                ys.append(0.0)
                zs.append(z)
                continue
            for angle in angles:
                xs.append(float(radius * np.cos(angle)))
                ys.append(float(radius * np.sin(angle)))
                zs.append(z)
    return np.asarray(xs), np.asarray(ys), np.asarray(zs)


def generate(
    geometry: CanisterGeometry = GAMMACELL_3000_ELAN,
    central_gy: float = 25.0,
    relative_uncertainty: float = 0.02,
    defect: str | None = None,
    seed: int = 0,
) -> DosePoints:
    """Build a deterministic point set.

    ``defect`` is ``None``, ``cold_spot`` (12 Gy near the bottom axis) or
    ``low_center`` (20 Gy at the mid-plane axis).
    """

    if defect not in (None, "cold_spot", "low_center"):
        raise ValueError("defect must be None, 'cold_spot' or 'low_center'.")
    x, y, z = sample_positions(geometry)
    dose = synthetic_dose_gy(x, y, z, geometry, central_gy)
    dose = _apply_defect(x, y, z, dose, geometry, defect)
    uncertainty = None
    if relative_uncertainty:
        if relative_uncertainty < 0:
            raise ValueError("relative_uncertainty cannot be negative.")
        uncertainty = np.abs(dose) * relative_uncertainty
        if seed:
            rng = np.random.default_rng(seed)
            dose = dose + rng.normal(0.0, uncertainty)
    return DosePoints(x, y, z, dose, uncertainty)


def _apply_defect(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    dose: np.ndarray,
    geometry: CanisterGeometry,
    defect: str | None,
) -> np.ndarray:
    if defect is None:
        return dose
    updated = np.array(dose, copy=True)
    radial = np.hypot(x, y)
    if defect == "cold_spot":
        updated[(z < 30.0) & (radial < 15.0)] = 12.0
        return updated
    centre = (radial < 1.0) & (np.abs(z - geometry.mid_height_mm) < 1.0)
    if not np.any(centre):
        raise ValueError("low_center requires a sample on the mid-plane axis.")
    updated[centre] = 20.0
    return updated
