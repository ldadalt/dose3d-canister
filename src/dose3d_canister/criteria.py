"""Dose bounds used to judge a canister map.

The numbers are the public criteria named in blood-irradiation practice.
They are configuration, not a clinical authorisation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DoseCriteria:
    """Bounds in gray. ``None`` means that bound is not part of the preset."""

    name: str
    dmin_gy: float | None = None
    dmax_gy: float | None = None
    central_plane_min_gy: float | None = None
    central_point_min_gy: float | None = None
    note: str = ""

    def __post_init__(self) -> None:
        for label, value in (
            ("dmin_gy", self.dmin_gy),
            ("dmax_gy", self.dmax_gy),
            ("central_plane_min_gy", self.central_plane_min_gy),
            ("central_point_min_gy", self.central_point_min_gy),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{label} cannot be negative.")
        if (
            self.dmin_gy is not None
            and self.dmax_gy is not None
            and self.dmax_gy < self.dmin_gy
        ):
            raise ValueError("dmax_gy is below dmin_gy.")


FDA_AABB = DoseCriteria(
    name="FDA/AABB",
    dmin_gy=15.0,
    central_plane_min_gy=25.0,
    central_point_min_gy=25.0,
    note=(
        "25 Gy at the centre of the canister and no less than 15 Gy "
        "anywhere in the irradiated volume."
    ),
)

PORTARIA_158 = DoseCriteria(
    name="Portaria MS 158/2016",
    dmin_gy=15.0,
    dmax_gy=50.0,
    central_plane_min_gy=25.0,
    note=(
        "Minimum not below 15 Gy, maximum not above 50 Gy, and mean dose "
        "on the central plane at least 25 Gy."
    ),
)

BCSH = DoseCriteria(
    name="BCSH",
    dmin_gy=25.0,
    dmax_gy=50.0,
    note="Minimum 25 Gy and maximum 50 Gy.",
)

JAPAN = DoseCriteria(
    name="Japan Guideline VI (2024)",
    dmin_gy=15.0,
    dmax_gy=50.0,
    note=(
        "Every part of the bag receives 15 Gy to 50 Gy. "
        "The centre is not required to be 25 Gy."
    ),
)

PRESETS: dict[str, DoseCriteria] = {
    "fda": FDA_AABB,
    "fda-aabb": FDA_AABB,
    "portaria158": PORTARIA_158,
    "portaria": PORTARIA_158,
    "bcsh": BCSH,
    "japan": JAPAN,
    "jrc": JAPAN,
}


def get_preset(name: str) -> DoseCriteria:
    key = name.strip().lower()
    try:
        return PRESETS[key]
    except KeyError as exc:
        known = ", ".join(sorted(set(PRESETS)))
        raise KeyError(f"Unknown criteria {name!r}. Known names: {known}.") from exc
