"""JSON history of canister mappings and the timer correction between them."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from dose3d_canister.decay import corrected_time_between


@dataclass(frozen=True)
class MappingRecord:
    measured_on: str
    irradiation_time_s: float
    central_dose_gy: float | None
    dmin_gy: float | None
    dmax_gy: float | None
    uniformity: float | None
    criteria: str
    passed: bool

    def on(self) -> date:
        return date.fromisoformat(self.measured_on)


def load_history(path: str | Path) -> list[MappingRecord]:
    file_path = Path(path)
    if not file_path.exists():
        return []
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    return [MappingRecord(**item) for item in payload]


def save_history(path: str | Path, records: list[MappingRecord]) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(record) for record in records]
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def append_record(path: str | Path, record: MappingRecord) -> list[MappingRecord]:
    records = load_history(path)
    records.append(record)
    records.sort(key=lambda item: item.measured_on)
    save_history(path, records)
    return records


def timer_after(previous: MappingRecord, later: date) -> float:
    """Irradiation time on ``later`` that matches ``previous`` central dose."""

    return corrected_time_between(previous.irradiation_time_s, previous.on(), later)
