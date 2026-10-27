# Example dose maps

## `synthetic_gammacell.csv`

Illustrative axisymmetric field used for demos. The centre is fixed at 25 Gy.
It is not a measurement.

## TLD grid sets A–E

Test sets transcribed from dose spreadsheets in gray.

- Rows run from the top of the spreadsheet to the bottom.
- Columns run left to right.
- The `*_matrix.csv` file keeps the raw integers.
- The point file places those values on the diametral plane `y = 0` of the
  Gammacell 3000 Elan canister: `x` from −61 mm to +61 mm, `z` from 193 mm
  (top of the sheet) down to 1 mm (bottom of the sheet).

Each spreadsheet is a plane. A rotating canister is treated as azimuthally
uniform, so reconstruction expands that plane around the axis:

```bash
dose3d-canister run examples/tld_grid_20x20.csv -o out/tld_grid --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_b_20x20.csv -o out/tld_grid_b --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_c_20x20.csv -o out/tld_grid_c --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_d_20x20.csv -o out/tld_grid_d --axisymmetric --criteria japan
dose3d-canister run examples/tld_grid_e_21x20.csv -o out/tld_grid_e --axisymmetric --criteria japan
```

| Set | File | Measured range | Notes |
| --- | --- | --- | --- |
| A | `tld_grid_20x20.csv` | 20–36 Gy | Upper centre near 20–21 Gy; walls at mid-height reach 36 Gy |
| B | `tld_grid_b_20x20.csv` | 21–36 Gy | Two cells at 21 Gy near the upper mid-plane; walls reach 36 Gy |
| C | `tld_grid_c_20x20.csv` | 16–43 Gy | Cold spots at 16 Gy and a hot wall peak at 43 Gy |
| D | `tld_grid_d_20x20.csv` | 14–37 Gy | Built from a 20×10 half-plane of decimals: values rounded to integers and mirrored wall→centre→wall |
| E | `tld_grid_e_21x20.csv` | 20–36 Gy | Same family as A, but 21×20: keeps the mid-height row `34,33,30…` that sits between the 35 Gy band and the red 36 Gy wall peak |

Sets A–C and E pass Japan and fail BCSH/EDQM on the minimum. Set D fails Japan too,
because the mirrored wall cold spot is 14 Gy.
