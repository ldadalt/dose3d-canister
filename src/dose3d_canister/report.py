"""One-page PDF with the numbers that have to travel with the figure."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from dose3d_canister.criteria import DoseCriteria
from dose3d_canister.geometry import CanisterGeometry
from dose3d_canister.interpolate import DoseVolume
from dose3d_canister.metrics import DoseMetrics
from dose3d_canister.view import _matplotlib_slices


def write_pdf(
    path: str | Path,
    geometry: CanisterGeometry,
    criteria: DoseCriteria,
    volume: DoseVolume,
    metrics: DoseMetrics,
) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    figure = _matplotlib_slices(volume)
    text = _report_text(geometry, criteria, metrics)
    figure.text(
        0.01,
        0.01,
        text,
        fontsize=8,
        family="monospace",
        va="bottom",
        transform=figure.transFigure,
    )
    figure.subplots_adjust(bottom=0.48)
    figure.savefig(file_path, format="pdf")
    plt.close(figure)


def _report_text(geometry: CanisterGeometry, criteria: DoseCriteria, metrics: DoseMetrics) -> str:
    lines = [
        f"{geometry.name}   D {geometry.inner_diameter_mm:.0f} mm   H {geometry.height_mm:.0f} mm",
        f"Criteria: {criteria.name}. {criteria.note}",
        (
            f"Measured Dmin/Dmax {_fmt(metrics.measured_dmin_gy)}/"
            f"{_fmt(metrics.measured_dmax_gy)} Gy"
            f"   uniformity {_fmt(metrics.uniformity_measured)}"
        ),
        (
            f"Reconstructed Dmin/Dmax {_fmt(metrics.reconstructed_dmin_gy)}/"
            f"{_fmt(metrics.reconstructed_dmax_gy)} Gy"
            f"   uniformity {_fmt(metrics.uniformity_reconstructed)}"
        ),
        (
            f"Central point {_fmt(metrics.central_point_gy)} Gy"
            f"   central-plane mean {_fmt(metrics.central_plane_mean_gy)} Gy"
            f"   volume >= Dmin {_fmt_fraction(metrics.volume_above_dmin_fraction)}"
        ),
        (
            f"Coverage {_fmt_fraction(metrics.coverage_fraction)}"
            f"   median distance to a sample {_fmt(metrics.median_nearest_mm)} mm"
            f"   median indicative u {_fmt(metrics.median_indicative_uncertainty_gy)} Gy"
        ),
        "Interpolation is not a measurement. Empty nodes were outside the sample hull.",
    ]
    for check in metrics.checks:
        lines.append(f"[{check.status}] {check.name}: {check.detail}")
    return "\n".join(lines)


def _fmt(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:.2f}"


def _fmt_fraction(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{100.0 * value:.1f}%"
