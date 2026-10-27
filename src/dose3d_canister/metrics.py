"""Dose summaries and criterion checks.

Measured values come from the input points. Reconstructed values come from
grid nodes that received a linear interpolant. A pass on those nodes does
not measure the unsampled volume.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.spatial import cKDTree

from dose3d_canister.criteria import DoseCriteria
from dose3d_canister.geometry import CanisterGeometry
from dose3d_canister.interpolate import DoseVolume, dose_at
from dose3d_canister.io import DosePoints


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "status": self.status, "detail": self.detail}


@dataclass(frozen=True)
class DoseMetrics:
    n_points: int
    measured_dmin_gy: float
    measured_dmax_gy: float
    measured_central_gy: float | None
    reconstructed_dmin_gy: float | None
    reconstructed_dmax_gy: float | None
    uniformity_measured: float | None
    uniformity_reconstructed: float | None
    central_point_gy: float | None
    central_plane_mean_gy: float | None
    volume_above_dmin_fraction: float | None
    coverage_fraction: float
    median_nearest_mm: float | None
    median_indicative_uncertainty_gy: float | None
    undersampled_fraction: float | None
    checks: list[Check] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(check.status != "fail" for check in self.checks)

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {}
        for key, value in self.__dict__.items():
            if key == "checks":
                payload[key] = [check.to_dict() for check in self.checks]
            else:
                payload[key] = _json_ready(value)
        payload["passed"] = self.passed
        return payload


def summarise(
    points: DosePoints,
    volume: DoseVolume,
    geometry: CanisterGeometry,
    criteria: DoseCriteria,
    plane_half_thickness_mm: float = 5.0,
    undersampled_factor: float = 1.5,
) -> DoseMetrics:
    reconstructed = volume.inside & np.isfinite(volume.dose_gy)
    coverage = float(reconstructed.sum() / volume.inside.sum()) if volume.inside.any() else 0.0
    measured_central = _measured_central(points, geometry)
    central_point = dose_at(points, (0.0, 0.0, geometry.mid_height_mm))
    if not np.isfinite(central_point):
        central_point_value: float | None = None
    else:
        central_point_value = float(central_point)

    plane = reconstructed & (np.abs(volume.z_mm[None, None, :] - geometry.mid_height_mm) <= plane_half_thickness_mm)
    plane_doses = volume.dose_gy[plane]
    plane_mean = float(plane_doses.mean()) if plane_doses.size else None

    rec_doses = volume.dose_gy[reconstructed]
    rec_min = float(rec_doses.min()) if rec_doses.size else None
    rec_max = float(rec_doses.max()) if rec_doses.size else None
    support = volume.nearest_mm[reconstructed]
    median_nearest = float(np.median(support)) if support.size else None
    uncertainty = volume.indicative_uncertainty_gy[reconstructed]
    finite_u = uncertainty[np.isfinite(uncertainty)]
    median_u = float(np.median(finite_u)) if finite_u.size else None

    sample_gaps = _nearest_sample_spacing(points)
    if median_nearest is None or sample_gaps is None:
        undersampled = None
    else:
        limit = undersampled_factor * sample_gaps
        undersampled = float(np.mean(support > limit))

    above = None
    if criteria.dmin_gy is not None and rec_doses.size:
        above = float(np.mean(rec_doses >= criteria.dmin_gy))

    metrics = DoseMetrics(
        n_points=len(points),
        measured_dmin_gy=float(points.dose_gy.min()),
        measured_dmax_gy=float(points.dose_gy.max()),
        measured_central_gy=measured_central,
        reconstructed_dmin_gy=rec_min,
        reconstructed_dmax_gy=rec_max,
        uniformity_measured=_ratio(float(points.dose_gy.max()), float(points.dose_gy.min())),
        uniformity_reconstructed=_ratio(rec_max, rec_min),
        central_point_gy=central_point_value,
        central_plane_mean_gy=plane_mean,
        volume_above_dmin_fraction=above,
        coverage_fraction=coverage,
        median_nearest_mm=median_nearest,
        median_indicative_uncertainty_gy=median_u,
        undersampled_fraction=undersampled,
    )
    return DoseMetrics(**{**metrics.__dict__, "checks": _checks(metrics, criteria)})


def _checks(metrics: DoseMetrics, criteria: DoseCriteria) -> list[Check]:
    checks: list[Check] = []
    checks.append(
        _bound(
            "measured minimum",
            metrics.measured_dmin_gy,
            criteria.dmin_gy,
            lower=True,
        )
    )
    checks.append(
        _bound(
            "measured maximum",
            metrics.measured_dmax_gy,
            criteria.dmax_gy,
            lower=False,
        )
    )
    checks.append(
        _bound(
            "reconstructed minimum",
            metrics.reconstructed_dmin_gy,
            criteria.dmin_gy,
            lower=True,
        )
    )
    checks.append(
        _bound(
            "reconstructed maximum",
            metrics.reconstructed_dmax_gy,
            criteria.dmax_gy,
            lower=False,
        )
    )
    central = metrics.measured_central_gy
    central_label = "measured central point"
    if central is None:
        central = metrics.central_point_gy
        central_label = "interpolated central point"
    checks.append(_bound(central_label, central, criteria.central_point_min_gy, lower=True))
    checks.append(
        _bound(
            "central-plane mean",
            metrics.central_plane_mean_gy,
            criteria.central_plane_min_gy,
            lower=True,
        )
    )
    return [check for check in checks if check.status != "absent"]


def _bound(name: str, value: float | None, limit: float | None, *, lower: bool) -> Check:
    if limit is None:
        return Check(name, "absent", "")
    if value is None or not np.isfinite(value):
        return Check(name, "not_evaluated", "No finite value was available.")
    ok = value >= limit if lower else value <= limit
    relation = ">=" if lower else "<="
    detail = f"{value:.3f} Gy {relation} {limit:.3f} Gy"
    return Check(name, "pass" if ok else "fail", detail)


def _ratio(high: float | None, low: float | None) -> float | None:
    if high is None or low is None or low <= 0 or not np.isfinite(low) or not np.isfinite(high):
        return None
    return float(high / low)


def _measured_central(points: DosePoints, geometry: CanisterGeometry) -> float | None:
    radial = np.hypot(points.x_mm, points.y_mm)
    mask = (radial <= 1.0) & (np.abs(points.z_mm - geometry.mid_height_mm) <= 1.0)
    if not np.any(mask):
        return None
    return float(points.dose_gy[mask].mean())


def _nearest_sample_spacing(points: DosePoints) -> float | None:
    if len(points) < 2:
        return None
    tree = cKDTree(points.xyz)
    distances = tree.query(points.xyz, k=2)[0][:, 1]
    return float(np.median(distances))


def _json_ready(value: object) -> object:
    if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
        return None
    return value
