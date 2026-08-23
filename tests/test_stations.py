"""`Complex` and `Station` are compared by identity,
which holds only because loading interns them.
"""

from pathlib import Path

from mta_od_data import DATA
from mta_od_data.analyze.common import Complex, Station

COMPLEXES = DATA / "complexes.csv"
STATIONS = DATA / "stations.csv"


def test_loading_twice_yields_the_same_objects() -> None:
    """A run loads each file once, but nothing enforces that, and a
    second load handing back equal-but-distinct objects would make
    every `==` and every dict lookup on them silently wrong."""
    complexes_by_id = Complex.load_all(COMPLEXES)
    again = Complex.load_all(COMPLEXES)
    assert all(a is b for a, b in zip(complexes_by_id, again, strict=True))

    stations = Station.load_all(STATIONS, complexes_by_id)
    # Against the *other* load's complexes, since a `Station` interns
    # by its fields and its complex is one of them.
    stations_again = Station.load_all(STATIONS, again)
    assert all(a is b for a, b in zip(stations, stations_again, strict=True))


def test_a_different_file_is_a_different_station(tmp_path: Path) -> None:
    """Interning is by value, not by id: ids are unique only within one
    station file, so a run passed its own `--stations` must not be
    handed the rows of whichever file happened to be read first."""
    edited = tmp_path / "complexes.csv"
    edited.write_text(COMPLEXES.read_text().replace("Astoria-Ditmars Blvd", "Ditmars"))
    complexes_by_id = Complex.load_all(COMPLEXES)
    others = Complex.load_all(edited)
    changed = [
        (mine, theirs)
        for mine, theirs in zip(complexes_by_id, others, strict=True)
        if mine is not theirs
    ]
    assert [mine.name for mine, _ in changed] == ["Astoria-Ditmars Blvd"]
    assert [theirs.name for _, theirs in changed] == ["Ditmars"]
