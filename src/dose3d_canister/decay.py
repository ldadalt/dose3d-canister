"""Cs-137 decay correction for the irradiation timer.

Delivering the same dose after the source has decayed takes a longer
irradiation. The scale factor is ``exp(ln(2) * elapsed / half_life)``.
"""

from __future__ import annotations

import math
from datetime import date

# NIST recommended half-life, rounded to two decimals. Override it if a
# calibration certificate quotes another value.
CS137_HALF_LIFE_YEARS = 30.08
DAYS_PER_YEAR = 365.2425
CS137_HALF_LIFE_DAYS = CS137_HALF_LIFE_YEARS * DAYS_PER_YEAR


def activity_ratio(elapsed_days: float, half_life_days: float = CS137_HALF_LIFE_DAYS) -> float:
    """Activity at the later time divided by activity at the earlier time."""

    if half_life_days <= 0:
        raise ValueError("half_life_days must be positive.")
    return math.exp(-math.log(2.0) * elapsed_days / half_life_days)


def irradiation_time_for_same_dose(
    previous_time_s: float,
    elapsed_days: float,
    half_life_days: float = CS137_HALF_LIFE_DAYS,
) -> float:
    """Timer setting that delivers the same dose after ``elapsed_days``."""

    if previous_time_s < 0:
        raise ValueError("previous_time_s cannot be negative.")
    ratio = activity_ratio(elapsed_days, half_life_days)
    if ratio == 0:
        raise ValueError("Activity ratio underflowed to zero.")
    return previous_time_s / ratio


def elapsed_days(earlier: date, later: date) -> int:
    return (later - earlier).days


def corrected_time_between(
    previous_time_s: float,
    earlier: date,
    later: date,
    half_life_days: float = CS137_HALF_LIFE_DAYS,
) -> float:
    return irradiation_time_for_same_dose(
        previous_time_s,
        elapsed_days(earlier, later),
        half_life_days,
    )
