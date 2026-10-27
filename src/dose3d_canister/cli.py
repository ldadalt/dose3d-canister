"""Command line for a synthetic map, a reconstruction, and a timer correction."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from dose3d_canister.axisymmetric import expand_axisymmetric
from dose3d_canister.criteria import get_preset
from dose3d_canister.decay import corrected_time_between
from dose3d_canister.geometry import GAMMACELL_3000_ELAN
from dose3d_canister.history import MappingRecord, append_record
from dose3d_canister.interpolate import reconstruct
from dose3d_canister.io import read_points, write_points
from dose3d_canister.metrics import summarise
from dose3d_canister.report import write_pdf
from dose3d_canister.synthetic import SYNTHETIC_NOTE, generate
from dose3d_canister.view import save_axial_gif, save_slice_png, write_html


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dose3d-canister",
        description="3D dose map inside a blood-irradiator canister.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    synthetic = commands.add_parser("synthetic", help="Write an illustrative CSV.")
    synthetic.add_argument("--output", "-o", type=Path, required=True)
    synthetic.add_argument("--central-gy", type=float, default=25.0)
    synthetic.add_argument("--defect", choices=("cold_spot", "low_center"), default=None)
    synthetic.set_defaults(func=_synthetic)

    run = commands.add_parser("run", help="Reconstruct a CSV and write the report.")
    run.add_argument("csv", type=Path)
    run.add_argument("--output", "-o", type=Path, required=True)
    run.add_argument("--criteria", default="fda-aabb")
    run.add_argument("--spacing-mm", type=float, default=2.0)
    run.add_argument(
        "--axisymmetric",
        action="store_true",
        help="Copy a diametral plane around the canister axis before reconstructing.",
    )
    run.add_argument(
        "--angles",
        type=int,
        default=16,
        help="Azimuth copies when --axisymmetric is set (more angles → smoother 3D shells).",
    )
    run.add_argument("--history", type=Path)
    run.add_argument("--date", type=date.fromisoformat)
    run.add_argument("--irradiation-time-s", type=float)
    run.set_defaults(func=_run)

    correct = commands.add_parser("correct-time", help="Scale a Cs-137 irradiation time.")
    correct.add_argument("--previous-seconds", type=float, required=True)
    correct.add_argument("--previous-date", type=date.fromisoformat, required=True)
    correct.add_argument("--date", type=date.fromisoformat, required=True)
    correct.set_defaults(func=_correct)

    args = parser.parse_args(argv)
    return int(args.func(args))


def _synthetic(args: argparse.Namespace) -> int:
    points = generate(central_gy=args.central_gy, defect=args.defect)
    write_points(args.output, points)
    print(SYNTHETIC_NOTE)
    print(args.output)
    return 0


def _run(args: argparse.Namespace) -> int:
    points = read_points(args.csv)
    if args.axisymmetric:
        points = expand_axisymmetric(points, n_angles=args.angles)
    try:
        criteria = get_preset(args.criteria)
    except KeyError as exc:
        raise SystemExit(str(exc)) from exc
    volume = reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=args.spacing_mm)
    metrics = summarise(points, volume, GAMMACELL_3000_ELAN, criteria)
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    (out / "metrics.json").write_text(json.dumps(metrics.to_dict(), indent=2), encoding="utf-8")
    write_html(
        volume,
        out / "dose3d.html",
        f"{GAMMACELL_3000_ELAN.name} — {criteria.name}",
        criteria=criteria,
    )
    save_slice_png(volume, out / "slices.png")
    write_pdf(out / "report.pdf", GAMMACELL_3000_ELAN, criteria, volume, metrics)
    if args.history is not None:
        if args.date is None or args.irradiation_time_s is None:
            raise SystemExit("--history requires --date and --irradiation-time-s.")
        append_record(
            args.history,
            MappingRecord(
                measured_on=args.date.isoformat(),
                irradiation_time_s=args.irradiation_time_s,
                central_dose_gy=metrics.measured_central_gy
                if metrics.measured_central_gy is not None
                else metrics.central_point_gy,
                dmin_gy=metrics.measured_dmin_gy,
                dmax_gy=metrics.measured_dmax_gy,
                uniformity=metrics.uniformity_measured,
                criteria=criteria.name,
                passed=metrics.passed,
            ),
        )
    print(json.dumps({"passed": metrics.passed, "output": str(out)}, indent=2))
    return 0 if metrics.passed else 2


def _correct(args: argparse.Namespace) -> int:
    updated = corrected_time_between(args.previous_seconds, args.previous_date, args.date)
    print(
        json.dumps(
            {
                "previous_seconds": args.previous_seconds,
                "corrected_seconds": updated,
                "ratio": updated / args.previous_seconds if args.previous_seconds else None,
            },
            indent=2,
        )
    )
    return 0
