"""`Complex` and `Station` are compared by identity,
which holds only because loading interns them.

Skipped without the station reference CSVs, which are gitignored.
"""

from pathlib import Path

import pytest

from mta_od_data import DATA, ROOT
from mta_od_data.analyze.common import Complex, Station

STATIONS = DATA / "stations_complexes.csv"
STATIONS_INDIVIDUAL = DATA / "stations_individual.csv"

pytestmark = pytest.mark.skipif(
    not (STATIONS.exists() and STATIONS_INDIVIDUAL.exists()),
    reason=(
        f"{STATIONS.relative_to(ROOT)}/{STATIONS_INDIVIDUAL.relative_to(ROOT)} not "
        "found (run `uv run mta-od-data prepare` first)"
    ),
)


def test_loading_twice_yields_the_same_objects() -> None:
    """A run loads each file once, but nothing enforces that, and a
    second load handing back equal-but-distinct objects would make
    every `==` and every dict lookup on them silently wrong."""
    complexes = Complex.load_all(STATIONS)
    again = Complex.load_all(STATIONS)
    assert all(complexes[cid] is again[cid] for cid in complexes)

    stations = Station.load_all(STATIONS_INDIVIDUAL, complexes)
    # Against the *other* load's complexes, since a `Station` interns
    # by its fields and its complex is one of them.
    stations_again = Station.load_all(STATIONS_INDIVIDUAL, again)
    assert all(a is b for a, b in zip(stations, stations_again, strict=True))


def test_a_different_file_is_a_different_station(tmp_path: Path) -> None:
    """Interning is by value, not by id: ids are unique only within one
    station file, so a run passed its own `--stations` must not be
    handed the rows of whichever file happened to be read first."""
    edited = tmp_path / "stations_complexes.csv"
    edited.write_text(STATIONS.read_text().replace("Astoria-Ditmars Blvd", "Ditmars"))
    complexes = Complex.load_all(STATIONS)
    others = Complex.load_all(edited)
    changed = [cid for cid in complexes if complexes[cid] is not others[cid]]
    assert [complexes[cid].name for cid in changed] == ["Astoria-Ditmars Blvd"]
    assert [others[cid].name for cid in changed] == ["Ditmars"]
