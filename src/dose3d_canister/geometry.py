"""Canister volume used to clip the reconstruction.

The internal cylinder matches the Gammacell 3000 Elan canister published by
Best Theratronics: 124 mm internal diameter, 194 mm internal height, 2.34 L.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

_GAMMACELL_VOLUME_L = np.pi * (62.0 / 1000.0) ** 2 * (194.0 / 1000.0) * 1000.0


@dataclass(frozen=True)
class CanisterGeometry:
    """Right circular cylinder. Origin on the axis, z = 0 at the bottom."""

    name: str
    inner_diameter_mm: float
    height_mm: float
    source: str

    def __post_init__(self) -> None:
        if self.inner_diameter_mm <= 0 or self.height_mm <= 0:
            raise ValueError("Canister diameter and height must be positive.")

    @property
    def inner_radius_mm(self) -> float:
        return self.inner_diameter_mm / 2.0

    @property
    def mid_height_mm(self) -> float:
        return self.height_mm / 2.0

    @property
    def volume_l(self) -> float:
        radius_m = self.inner_radius_mm / 1000.0
        height_m = self.height_mm / 1000.0
        return float(np.pi * radius_m**2 * height_m * 1000.0)


GAMMACELL_3000_ELAN = CanisterGeometry(
    name="Gammacell 3000 Elan",
    inner_diameter_mm=124.0,
    height_mm=194.0,
    source=(
        "Best Theratronics brochure: internal canister diameter 124 mm, "
        "internal height 194 mm, volume 2.34 L."
    ),
)


def inside_canister(
    x_mm: np.ndarray,
    y_mm: np.ndarray,
    z_mm: np.ndarray,
    geometry: CanisterGeometry,
    *,
    radial_tolerance_mm: float = 1e-6,
) -> np.ndarray:
    """Return a boolean mask of points inside or on the inner cylinder."""

    radius = np.hypot(np.asarray(x_mm, dtype=float), np.asarray(y_mm, dtype=float))
    z = np.asarray(z_mm, dtype=float)
    limit = geometry.inner_radius_mm + radial_tolerance_mm
    return (radius <= limit) & (z >= -radial_tolerance_mm) & (z <= geometry.height_mm + radial_tolerance_mm)


def assert_volume_matches_brochure(tolerance_l: float = 0.02) -> None:
    """The published 2.34 L follows from the internal diameter and height."""

    if abs(GAMMACELL_3000_ELAN.volume_l - 2.34) > tolerance_l:
        raise AssertionError(
            f"Computed volume {GAMMACELL_3000_ELAN.volume_l:.3f} L is far from 2.34 L."
        )
    if abs(_GAMMACELL_VOLUME_L - GAMMACELL_3000_ELAN.volume_l) > 1e-9:
        raise AssertionError("Volume helper drifted from the geometry property.")
