from __future__ import annotations

import json
from dataclasses import replace
from datetime import date

import numpy as np
import pytest

from dose3d_canister.axisymmetric import expand_axisymmetric
from dose3d_canister.cli import main
from dose3d_canister.criteria import BCSH, FDA_AABB, JAPAN, PORTARIA_158, get_preset
from dose3d_canister.decay import (
    CS137_HALF_LIFE_DAYS,
    activity_ratio,
    corrected_time_between,
    irradiation_time_for_same_dose,
)
from dose3d_canister.geometry import GAMMACELL_3000_ELAN, inside_canister
from dose3d_canister.history import MappingRecord, append_record, load_history, timer_after
from dose3d_canister.interpolate import reconstruct
from dose3d_canister.io import DosePoints, read_points, write_points
from dose3d_canister.metrics import summarise
from dose3d_canister.synthetic import generate, synthetic_dose_gy


@pytest.mark.parametrize(
    ("filename", "n_points", "dmin", "dmax", "japan_passes"),
    [
        ("tld_grid_20x20.csv", 400, 20.0, 36.0, True),
        ("tld_grid_b_20x20.csv", 400, 21.0, 36.0, True),
        ("tld_grid_c_20x20.csv", 400, 16.0, 43.0, True),
        ("tld_grid_d_20x20.csv", 400, 14.0, 37.0, False),
        ("tld_grid_e_21x20.csv", 420, 20.0, 36.0, True),
    ],
)
def test_tld_grid_example_reconstructs_when_expanded(
    filename: str, n_points: int, dmin: float, dmax: float, japan_passes: bool
) -> None:
    from pathlib import Path

    csv_path = Path(__file__).resolve().parents[1] / "examples" / filename
    points = read_points(csv_path)
    assert len(points) == n_points
    assert points.dose_gy.min() == dmin
    assert points.dose_gy.max() == dmax
    with pytest.raises(ValueError, match="coplanar"):
        reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=8.0)
    expanded = expand_axisymmetric(points, n_angles=6)
    volume = reconstruct(expanded, GAMMACELL_3000_ELAN, spacing_mm=8.0)
    japan = summarise(expanded, volume, GAMMACELL_3000_ELAN, JAPAN)
    europe = summarise(expanded, volume, GAMMACELL_3000_ELAN, BCSH)
    assert japan.passed is japan_passes
    assert not europe.passed
    assert japan.measured_dmin_gy == dmin
    assert japan.measured_dmax_gy == dmax


def test_tld_grid_d_is_left_right_symmetric() -> None:
    from pathlib import Path

    full = np.loadtxt(
        Path(__file__).resolve().parents[1] / "examples" / "tld_grid_d_20x20_matrix.csv",
        delimiter=",",
    )
    assert full.shape == (20, 20)
    assert np.array_equal(full[:, :10], full[:, 10:][:, ::-1])


def test_clinical_isodose_levels_use_the_standard_gray_lines() -> None:
    from dose3d_canister.view import clinical_isodose_levels

    wide = np.array([12.0, 22.0, 33.0, 55.0])
    assert clinical_isodose_levels(wide) == [15, 20, 25, 30, 35, 40, 45, 50]
    narrow = np.array([22.0, 28.0, 31.0])
    assert clinical_isodose_levels(narrow) == [25.0, 30.0]


def test_canister_volume_matches_the_brochure() -> None:
    assert abs(GAMMACELL_3000_ELAN.volume_l - 2.34) < 0.01
    assert inside_canister(np.array([0.0]), np.array([0.0]), np.array([97.0]), GAMMACELL_3000_ELAN)
    assert not inside_canister(np.array([70.0]), np.array([0.0]), np.array([97.0]), GAMMACELL_3000_ELAN)


def test_centre_is_25_gy_and_the_wall_is_higher() -> None:
    centre = synthetic_dose_gy(np.array([0.0]), np.array([0.0]), np.array([97.0]))
    wall = synthetic_dose_gy(np.array([62.0]), np.array([0.0]), np.array([97.0]))
    assert centre[0] == pytest.approx(25.0)
    assert wall[0] > centre[0]


def test_linear_map_stays_inside_the_measured_range() -> None:
    points = generate(relative_uncertainty=0.0)
    volume = reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=4.0)
    reconstructed = volume.dose_gy[np.isfinite(volume.dose_gy)]
    assert reconstructed.min() >= points.dose_gy.min() - 1e-6
    assert reconstructed.max() <= points.dose_gy.max() + 1e-6
    assert volume.inside.sum() > reconstructed.size
    metrics = summarise(points, volume, GAMMACELL_3000_ELAN, FDA_AABB)
    assert metrics.passed
    assert metrics.measured_central_gy == pytest.approx(25.0)
    assert metrics.coverage_fraction < 1.0
    assert metrics.volume_above_dmin_fraction == pytest.approx(1.0)


def test_cold_spot_fails_the_minimum() -> None:
    points = generate(relative_uncertainty=0.0, defect="cold_spot")
    volume = reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=4.0)
    metrics = summarise(points, volume, GAMMACELL_3000_ELAN, FDA_AABB)
    assert metrics.measured_dmin_gy == pytest.approx(12.0)
    assert not metrics.passed


def test_low_centre_fails_only_the_central_requirement() -> None:
    points = generate(relative_uncertainty=0.0, defect="low_center")
    volume = reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=4.0)
    metrics = summarise(points, volume, GAMMACELL_3000_ELAN, FDA_AABB)
    assert metrics.measured_dmin_gy > 15.0
    assert metrics.measured_central_gy == pytest.approx(20.0)
    assert not metrics.passed


def test_low_centre_passes_japan_and_fails_the_american_centre() -> None:
    points = generate(relative_uncertainty=0.0, defect="low_center")
    volume = reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=4.0)
    japan = summarise(points, volume, GAMMACELL_3000_ELAN, JAPAN)
    america = summarise(points, volume, GAMMACELL_3000_ELAN, FDA_AABB)
    assert get_preset("japan") is JAPAN
    assert get_preset("jrc") is JAPAN
    assert japan.passed
    assert not america.passed
    assert "central" not in {check.name for check in japan.checks}


def test_japan_rejects_a_dose_outside_15_to_50_gy() -> None:
    cold = generate(relative_uncertainty=0.0, defect="cold_spot")
    cold_volume = reconstruct(cold, GAMMACELL_3000_ELAN, spacing_mm=8.0)
    assert not summarise(cold, cold_volume, GAMMACELL_3000_ELAN, JAPAN).passed

    hot = replace(generate(relative_uncertainty=0.0), dose_gy=generate().dose_gy * 3.0, uncertainty_gy=None)
    hot_volume = reconstruct(hot, GAMMACELL_3000_ELAN, spacing_mm=8.0)
    assert not summarise(hot, hot_volume, GAMMACELL_3000_ELAN, JAPAN).passed


def test_scaled_field_fails_the_portaria_maximum() -> None:
    points = generate(relative_uncertainty=0.0)
    hot = replace(points, dose_gy=points.dose_gy * 3.0, uncertainty_gy=None)
    volume = reconstruct(hot, GAMMACELL_3000_ELAN, spacing_mm=8.0)
    metrics = summarise(hot, volume, GAMMACELL_3000_ELAN, PORTARIA_158)
    assert metrics.measured_dmax_gy > 50.0
    assert not metrics.passed


def test_points_outside_or_degenerate_are_rejected() -> None:
    outside = DosePoints(
        np.array([0.0, 80.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 10.0, 0.0]),
        np.array([10.0, 10.0, 10.0, 20.0]),
        np.ones(4),
    )
    with pytest.raises(ValueError, match="outside"):
        reconstruct(outside, GAMMACELL_3000_ELAN, spacing_mm=8.0)

    flat = DosePoints(np.array([0.0, 10.0, 0.0, -10.0]), np.array([0.0, 0.0, 10.0, 0.0]), np.full(4, 97.0), np.ones(4))
    with pytest.raises(ValueError, match="coplanar"):
        reconstruct(flat, GAMMACELL_3000_ELAN, spacing_mm=8.0)


def test_csv_roundtrip(tmp_path) -> None:
    points = generate()
    path = tmp_path / "map.csv"
    write_points(path, points)
    loaded = read_points(path)
    assert loaded.dose_gy == pytest.approx(points.dose_gy, rel=1e-5)
    assert loaded.uncertainty_gy is not None


def test_half_life_doubles_the_irradiation_time() -> None:
    assert activity_ratio(CS137_HALF_LIFE_DAYS) == pytest.approx(0.5)
    assert irradiation_time_for_same_dose(336.0, CS137_HALF_LIFE_DAYS) == pytest.approx(672.0)
    earlier = date(2026, 1, 1)
    later = date.fromordinal(earlier.toordinal() + round(CS137_HALF_LIFE_DAYS))
    assert corrected_time_between(100.0, earlier, later) == pytest.approx(200.0, rel=1e-3)


def test_history_orders_records_and_corrects_the_timer(tmp_path) -> None:
    path = tmp_path / "history.json"
    first = MappingRecord("2026-01-15", 336.0, 25.0, 22.0, 32.0, 1.45, "FDA/AABB", True)
    second = MappingRecord("2026-06-01", 340.0, 25.0, 22.0, 32.0, 1.45, "FDA/AABB", True)
    append_record(path, second)
    append_record(path, first)
    loaded = load_history(path)
    assert [item.measured_on for item in loaded] == ["2026-01-15", "2026-06-01"]
    assert timer_after(loaded[0], date(2026, 6, 1)) > 336.0


def test_unknown_criteria_name() -> None:
    with pytest.raises(KeyError):
        get_preset("nope")


def test_cli_writes_report_and_returns_failure_for_a_cold_spot(tmp_path) -> None:
    csv_path = tmp_path / "synthetic.csv"
    out = tmp_path / "out"
    assert main(["synthetic", "-o", str(csv_path)]) == 0
    assert main(["run", str(csv_path), "-o", str(out), "--spacing-mm", "4"]) == 0
    payload = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    assert payload["passed"] is True
    assert (out / "report.pdf").stat().st_size > 0
    html = (out / "dose3d.html").read_text(encoding="utf-8")
    assert "plotly" in html.lower()
    assert "Isodose" in html and "3D" in html
    assert (out / "slices.png").stat().st_size > 0

    cold = tmp_path / "cold.csv"
    assert main(["synthetic", "-o", str(cold), "--defect", "cold_spot"]) == 0
    assert main(["run", str(cold), "-o", str(tmp_path / "cold-out"), "--spacing-mm", "8"]) == 2


def test_cli_correct_time_prints_a_longer_setting(capsys) -> None:
    code = main(
        [
            "correct-time",
            "--previous-seconds",
            "336",
            "--previous-date",
            "2026-01-01",
            "--date",
            "2027-01-01",
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["corrected_seconds"] > 336
