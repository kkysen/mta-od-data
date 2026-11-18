"""`routed` routes again only when what it reads changes, with the routing faked."""

from datetime import date
from pathlib import Path

import pytest

from mta_od_data import builds
from mta_od_data.builds import routed


@pytest.fixture
def runs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """Each run routed, into a cache and from inputs of its own."""
    inputs = tmp_path / "inputs"
    (inputs / "gtfs").mkdir(parents=True)
    (inputs / "gtfs" / "feed.zip").write_bytes(b"feed")
    (inputs / "od.parquet").write_bytes(b"od")
    for name in ["stations.csv", "access.csv", "platform_edges.csv", "streets.osm.pbf"]:
        (inputs / name).write_text(name)
    # Alone, as `raptor` reads the platform CSVs beside it.
    (inputs / "platforms").mkdir()
    (inputs / "platforms" / "platforms.csv").write_text("platforms")
    monkeypatch.setattr(builds, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(builds, "gtfs_feeds", lambda: inputs / "gtfs")
    monkeypatch.setattr(builds, "od_parquet", lambda: inputs / "od.parquet")

    def streets(stations: Path) -> Path:
        return inputs / "streets.osm.pbf"

    monkeypatch.setattr(builds, "streets", streets)
    monkeypatch.setattr(builds, "DEFAULT_STATIONS", inputs / "stations.csv")
    monkeypatch.setattr(
        builds, "DEFAULT_PLATFORMS", inputs / "platforms" / "platforms.csv"
    )
    monkeypatch.setattr(builds, "DEFAULT_ACCESS", inputs / "access.csv")
    built: list[Path] = []

    def route_range(start: date, *args: object) -> Path:
        *_, out_dir, named = args
        assert isinstance(out_dir, Path) and isinstance(named, Path)
        built.append(named)
        out_dir.mkdir()
        (out_dir / "manifest.csv").write_text(f"date\n{start}\n")
        return out_dir / "manifest.csv"

    monkeypatch.setattr(builds, "route_range", route_range)
    return built


def test_routed_once(runs: list[Path], tmp_path: Path) -> None:
    manifest = routed()
    assert routed() == manifest
    assert runs == [manifest.parent]
    assert manifest.parent.parent == tmp_path / "cache" / "routing"
    assert manifest.read_text() == "date\n2025-08-11\n"


def test_routed_again_when_inputs_change(runs: list[Path], tmp_path: Path) -> None:
    first = routed()
    (tmp_path / "inputs" / "stations.csv").write_text("other stations")
    second = routed()
    assert second != first
    assert runs == [first.parent, second.parent]
    # The first is kept, and read again for its own inputs.
    (tmp_path / "inputs" / "stations.csv").write_text("stations.csv")
    assert routed() == first
    assert len(runs) == 2


def test_flags_and_dates_are_their_own_runs(runs: list[Path]) -> None:
    plain = routed()
    walked = routed(street_walks=True)
    shorter = routed(end=date(2025, 9, 30))
    assert len({plain, walked, shorter}) == 3
    assert len(runs) == 3


def test_entrances_only_with_street_walks(runs: list[Path], tmp_path: Path) -> None:
    plain = routed()
    walked = routed(street_walks=True)
    (tmp_path / "inputs" / "access.csv").write_text("other times")
    assert routed() == plain
    assert routed(street_walks=True) != walked
