"""CSV exchange for discrete canister measurements.

Columns are ``x_mm``, ``y_mm``, ``z_mm`` and ``dose_gy``.
``uncertainty_gy`` is optional (one standard deviation, same unit as dose).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

REQUIRED = ("x_mm", "y_mm", "z_mm", "dose_gy")
OPTIONAL = "uncertainty_gy"


@dataclass(frozen=True)
class DosePoints:
    x_mm: np.ndarray
    y_mm: np.ndarray
    z_mm: np.ndarray
    dose_gy: np.ndarray
    uncertainty_gy: np.ndarray | None = None

    def __post_init__(self) -> None:
        arrays = [self.x_mm, self.y_mm, self.z_mm, self.dose_gy]
        if any(np.asarray(item).shape != np.asarray(self.x_mm).shape for item in arrays):
            raise ValueError("Point arrays must share one shape.")
        if self.x_mm.ndim != 1:
            raise ValueError("Point arrays must be one-dimensional.")
        if not np.isfinite(self.xyz).all() or not np.isfinite(self.dose_gy).all():
            raise ValueError("Coordinates and dose must be finite.")
        if self.uncertainty_gy is not None:
            if self.uncertainty_gy.shape != self.dose_gy.shape:
                raise ValueError("uncertainty_gy must match the dose array.")
            if not np.isfinite(self.uncertainty_gy).all() or np.any(self.uncertainty_gy < 0):
                raise ValueError("uncertainty_gy must be finite and >= 0.")

    @property
    def xyz(self) -> np.ndarray:
        return np.column_stack([self.x_mm, self.y_mm, self.z_mm])

    def __len__(self) -> int:
        return int(self.dose_gy.size)


def read_points(path: str | Path) -> DosePoints:
    file_path = Path(path)
    with file_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{file_path} has no header.")
        fields = [name.strip() for name in reader.fieldnames]
        missing = [name for name in REQUIRED if name not in fields]
        if missing:
            raise ValueError(f"{file_path} is missing columns: {', '.join(missing)}.")
        rows = list(reader)

    if not rows:
        raise ValueError(f"{file_path} has no data rows.")

    def column(name: str) -> np.ndarray:
        try:
            return np.array([float(row[name]) for row in rows], dtype=float)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Column {name} in {file_path} is not numeric.") from exc

    uncertainty = column(OPTIONAL) if OPTIONAL in fields and any(row.get(OPTIONAL) for row in rows) else None
    return DosePoints(
        x_mm=column("x_mm"),
        y_mm=column("y_mm"),
        z_mm=column("z_mm"),
        dose_gy=column("dose_gy"),
        uncertainty_gy=uncertainty,
    )


def write_points(path: str | Path, points: DosePoints) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(REQUIRED)
    if points.uncertainty_gy is not None:
        fieldnames.append(OPTIONAL)
    with file_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(len(points)):
            row = {
                "x_mm": _format(points.x_mm[index]),
                "y_mm": _format(points.y_mm[index]),
                "z_mm": _format(points.z_mm[index]),
                "dose_gy": _format(points.dose_gy[index]),
            }
            if points.uncertainty_gy is not None:
                row[OPTIONAL] = _format(points.uncertainty_gy[index])
            writer.writerow(row)


def _format(value: float) -> str:
    return f"{float(value):.6g}"
