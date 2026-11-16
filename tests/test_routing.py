"""`route_range`'s manifest, with the routing itself faked."""

from csv import DictReader
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pytest

from mta_od_data import routing
from mta_od_data.routing import route_range


@dataclass(frozen=True, slots=True)
class FakeVersion:
    path: Path


@dataclass(frozen=True, slots=True)
class FakeSummary:
    path_texts: Path
    report: str = "routed\n"
    riders_in: float = 1.0
    riders_assigned: float = 1.0
    unassigned_no_stops: float = 0.0
    unassigned_unreachable: float = 0.0
    unassigned_no_departure: float = 0.0


def test_manifest_names_files_where_they_will_be(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    feed = FakeVersion(tmp_path / "gtfs" / "feed.zip")
    days = [(date(2025, 9, 17), feed, 4), (date(2025, 9, 18), feed, 5)]

    def load_versions(gtfs_dir: Path) -> list[FakeVersion]:
        return [feed]

    def pick_weekdays(
        versions: list[FakeVersion], start: date, end: date
    ) -> list[tuple[date, FakeVersion, int]]:
        return days

    def assign_dates(
        jobs: list[tuple[FakeVersion, date, Path]], *_: object
    ) -> list[FakeSummary]:
        return [
            FakeSummary(out.with_name(f"path-texts-{day}.parquet"))
            for _, day, out in jobs
        ]

    monkeypatch.setattr(routing, "load_versions", load_versions)
    monkeypatch.setattr(routing, "pick_weekdays", pick_weekdays)
    monkeypatch.setattr(routing, "assign_dates", assign_dates)
    building = tmp_path / "abc.partial"
    final = tmp_path / "abc"
    manifest = route_range(
        date(2025, 9, 1),
        date(2025, 9, 30),
        tmp_path / "gtfs",
        tmp_path / "od.parquet",
        tmp_path / "stations.csv",
        tmp_path / "platforms.csv",
        tmp_path / "assign.json5",
        1,
        None,
        building,
        named=final,
    )
    assert manifest == building / "manifest.csv"
    rows = list(DictReader(manifest.open()))
    assert [(r["date"], r["days"], r["day_of_week"]) for r in rows] == [
        ("2025-09-17", "4", "Wednesday"),
        ("2025-09-18", "5", "Thursday"),
    ]
    assert rows[0]["paths"] == str(final / "paths-2025-09-17.parquet")
    assert rows[0]["path_texts"] == str(final / "path-texts-2025-09-17.parquet")
    assert rows[0]["trips"] == str(final / "trips-2025-09-17.parquet")
