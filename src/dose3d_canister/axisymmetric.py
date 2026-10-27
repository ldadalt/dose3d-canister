"""Fill the canister from a diametral plane when the canister rotates.

A spreadsheet map is usually one vertical cut through the axis. With a
turning canister the dose is treated as the same at every azimuth, so the
plane is copied around the z axis. That step is an assumption, not a second
measurement.
"""

from __future__ import annotations

import numpy as np

from dose3d_canister.io import DosePoints


def expand_axisymmetric(points: DosePoints, n_angles: int = 8) -> DosePoints:
    """Copy the sample cloud around the canister axis.

    Angles are spaced over a half-turn when the plane already spans both
    sides of the axis (negative and positive x). Otherwise a full turn is
    used. The original points are kept.
    """

    if n_angles < 2:
        raise ValueError("n_angles must be at least 2.")
    if len(points) == 0:
        raise ValueError("No points to expand.")

    span_both_sides = bool(np.any(points.x_mm < 0.0) and np.any(points.x_mm > 0.0))
    period = np.pi if span_both_sides else 2.0 * np.pi
    angles = np.linspace(0.0, period, n_angles, endpoint=False)[1:]

    xs = [points.x_mm]
    ys = [points.y_mm]
    zs = [points.z_mm]
    doses = [points.dose_gy]
    uncertainties = [points.uncertainty_gy] if points.uncertainty_gy is not None else None

    for angle in angles:
        cos_a = float(np.cos(angle))
        sin_a = float(np.sin(angle))
        xs.append(points.x_mm * cos_a - points.y_mm * sin_a)
        ys.append(points.x_mm * sin_a + points.y_mm * cos_a)
        zs.append(points.z_mm)
        doses.append(points.dose_gy)
        if uncertainties is not None:
            uncertainties.append(points.uncertainty_gy)

    return DosePoints(
        x_mm=np.concatenate(xs),
        y_mm=np.concatenate(ys),
        z_mm=np.concatenate(zs),
        dose_gy=np.concatenate(doses),
        uncertainty_gy=None if uncertainties is None else np.concatenate(uncertainties),
    )
