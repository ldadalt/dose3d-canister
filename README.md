# Dose 3D canister

Reconstruct a three-dimensional dose map inside a blood-irradiator canister
from discrete dosimeter points (TLD, OSL or film samples).

The default volume is the **Gammacell 3000 Elan** canister published by Best
Theratronics: internal diameter 124 mm, internal height 194 mm, volume 2.34 L.
The canister turns between fixed Cs-137 sources. A typical vendor map with
25 Gy at the centre is about 19 Gy minimum and 33 Gy maximum.

This package does not run a Monte Carlo transport. It interpolates the points
you give it, reports the usual blood-irradiation comparisons, and scales the
irradiation timer for Cs-137 decay between mappings.

## What it will not tell you

Linear interpolation inside the convex hull of the samples cannot see a hot
or cold spot that sits between the dosimeters. Nodes outside that hull are
left empty. The coverage fraction, the distance to the nearest sample and the
indicative uncertainty are there so a smooth picture is not mistaken for a
measurement.

The indicative uncertainty combines the input standard deviation with a term
that grows when neighbouring samples disagree and the node is far from them.
It is a display model, not a GUM uncertainty budget.

Do not use the output as a clinical release decision. The synthetic generator
is an illustration: the centre is fixed at 25 Gy, the wall is higher and the
ends are lower. It is not a measured map and not a transport result.

## Criteria

| Preset | Command | Bounds |
| --- | --- | --- |
| FDA/AABB | `--criteria fda-aabb` (default) | ≥ 25 Gy at the centre, ≥ 15 Gy in the volume |
| Portaria MS 158/2016 | `--criteria portaria158` | 15 Gy to 50 Gy, central-plane mean ≥ 25 Gy |
| BCSH | `--criteria bcsh` | 25 Gy to 50 Gy |
| Japan Guideline VI (2024) | `--criteria japan` | 15 Gy to 50 Gy at every point; the centre is not required to be 25 Gy |

`run` exits with status 2 when a configured bound fails.

## Install

```bash
pip install -e ".[dev]"
```

Python 3.11 or newer.

## Commands

```bash
dose3d-canister synthetic -o examples/synthetic_gammacell.csv
dose3d-canister run examples/synthetic_gammacell.csv -o out
dose3d-canister run examples/tld_grid_20x20.csv -o out/tld_grid --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_b_20x20.csv -o out/tld_grid_b --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_c_20x20.csv -o out/tld_grid_c --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_d_20x20.csv -o out/tld_grid_d --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_e_21x20.csv -o out/tld_grid_e --axisymmetric --criteria japan
dose3d-canister correct-time --previous-seconds 336 --previous-date 2026-01-15 --date 2026-10-27
```

`examples/tld_grid_*.csv` are spreadsheets on the diametral plane of the
canister: A 20–36 Gy, B 21–36 Gy, C 16–43 Gy, D 14–37 Gy, E 20–36 Gy on a
21×20 grid. `--axisymmetric` copies that plane around the axis because a
turning canister is treated as azimuthally uniform. See `examples/README.md`.

`run` writes `metrics.json`, `dose3d.html` (labeled isodose curves and a 3D
model at 15–50 Gy), `slices.png` and `report.pdf`. Pass `--history mappings.json --date YYYY-MM-DD
--irradiation-time-s 336` to append that mapping.

The Cs-137 half-life used for the timer is 30.08 years. One half-life later
the same dose needs twice the irradiation time.

The committed synthetic map pins the centre at 25 Gy. On that illustration
the wall reaches about 32 Gy and the ends of the axis stay near 22 Gy, so
the FDA/AABB preset passes. About 9% of the canister nodes stay empty
because they lie outside the convex hull of the samples.

![Axial and coronal slices of the illustrative map](docs/images/slices.png)

![Axial sweep through the canister](docs/images/axial.gif)

CSV columns: `x_mm`, `y_mm`, `z_mm`, `dose_gy`, and optional `uncertainty_gy`.
The origin is on the canister axis and `z = 0` is the bottom.

## Library

```python
from dose3d_canister.criteria import FDA_AABB
from dose3d_canister.geometry import GAMMACELL_3000_ELAN
from dose3d_canister.interpolate import reconstruct
from dose3d_canister.io import read_points
from dose3d_canister.metrics import summarise

points = read_points("examples/synthetic_gammacell.csv")
volume = reconstruct(points, GAMMACELL_3000_ELAN, spacing_mm=2.0)
metrics = summarise(points, volume, GAMMACELL_3000_ELAN, FDA_AABB)
```

PyVista is an optional extra (`pip install -e ".[pyvista]"`).
`dose3d_canister.view.pyvista_cloud` builds a point cloud from the
reconstructed nodes.

## Development

```bash
pytest
```

## References

Dose criteria for Japan, the United States, Europe, Brazil, IAEA and ISO/ASTM are collected in [docs/referencias-irradiacao-de-sangue.md](docs/referencias-irradiacao-de-sangue.md). Canister dimensions and the shift from Cs-137 cylinders to X-ray chambers are in [docs/canisters-e-mercado.md](docs/canisters-e-mercado.md).

- Best Theratronics, Gammacell 1000 Elite / 3000 Elan brochure: internal canister 124 mm by 194 mm, 2.34 L, typical uniformity about 19 / 25 / 33 Gy when 25 Gy is delivered to the centre.
- FDA, 22 July 1993 memorandum: 25 Gy at the centre of the container and at least 15 Gy at any other point. No maximum is stated.
- EDQM Blood Guide, 22nd edition (2025), section 4.3.1.1, and the UK BSH 2020 guideline: no part of the component below 25 Gy or above 50 Gy.
- Brazilian Ministry of Health, Portaria GM/MS nº 158/2016, article 114: at least 25 Gy on the central plane, and no point below 15 Gy or above 50 Gy.

## License

MIT.
