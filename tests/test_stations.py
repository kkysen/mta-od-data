"""`Complex` and `Station` are compared by identity,
which holds only because loading interns them.
"""

from pathlib import Path

import pytest

from mta_od_data import DATA
from mta_od_data.analyze.common import (
    Complex,
    MissingComplex,
    MissingComplexError,
    Station,
    complexes_of,
)
from mta_od_data.analyze.deinterlining import resolve_pairs

COMPLEXES = DATA / "complexes.csv"
STATIONS = DATA / "stations.csv"


def test_loading_twice_yields_the_same_objects(tmp_path: Path) -> None:
    """A run loads each file once, but nothing enforces that, and a
    second load handing back equal-but-distinct objects would make
    every `==` and every dict lookup on them silently wrong.

    From a copy rather than twice from the one path, since loading is
    remembered by (path, text) and would otherwise hand back the first
    load itself, which is a different property and one the caching
    tests already cover.
    """
    copy = tmp_path / "complexes.csv"
    copy.write_text(COMPLEXES.read_text())
    complexes_by_id = Complex.load_all(COMPLEXES)
    again = Complex.load_all(copy)
    # The complexes themselves: the holes hold a `MissingComplex`,
    # which is built per load and isn't one.
    assert all(
        a is b
        for a, b in zip(complexes_of(complexes_by_id), complexes_of(again), strict=True)
    )

    stations = Station.load_all(STATIONS, complexes_by_id)
    # Against the *other* load's complexes, since a `Station` interns
    # by its fields and its complex is one of them.
    stations_again = Station.load_all(STATIONS, again)
    assert all(a is b for a, b in zip(stations, stations_again, strict=True))


def test_a_file_is_read_once_until_its_text_changes(tmp_path: Path) -> None:
    """What the cache is keyed by, in both shapes: a complex file by
    its path and text, since a hole in it holds the path to name, and a
    station file by its text and the complexes it resolves against."""
    complexes_path = tmp_path / "complexes.csv"
    complexes_path.write_text(COMPLEXES.read_text())
    stations_path = tmp_path / "stations.csv"
    stations_path.write_text(STATIONS.read_text())

    complexes_by_id = Complex.load_all(complexes_path)
    assert Complex.load_all(complexes_path) is complexes_by_id
    stations = Station.load_all(stations_path, complexes_by_id)
    assert Station.load_all(stations_path, complexes_by_id) is stations

    complexes_path.write_text(
        COMPLEXES.read_text().replace("Astoria-Ditmars Blvd", "Ditmars")
    )
    rewritten = Complex.load_all(complexes_path)
    assert rewritten is not complexes_by_id
    # And the stations with them, the complexes being half of their key.
    assert Station.load_all(stations_path, rewritten) is not stations


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
        for mine, theirs in zip(
            complexes_of(complexes_by_id), complexes_of(others), strict=True
        )
        if mine is not theirs
    ]
    assert [mine.name for mine, _ in changed] == ["Astoria-Ditmars Blvd"]
    assert [theirs.name for _, theirs in changed] == ["Ditmars"]


def test_an_id_no_complex_has_says_so_when_read() -> None:
    """The holes in `ComplexesById` are what let it be a tuple of
    `Complex`, so nothing tests for one: reading a field of one has to
    be what says the complex file is out of date."""
    complexes_by_id = Complex.load_all(COMPLEXES)
    holes = [c for c in complexes_by_id if isinstance(c, MissingComplex)]
    assert holes, "the real complex file has gaps in its ids"
    with pytest.raises(MissingComplexError, match="refetch station reference data"):
        holes[0].display()


def test_an_id_past_the_last_one_is_named(tmp_path: Path) -> None:
    """The one case an index can't answer for, so `resolve_pairs`
    catches the `IndexError` and says which id it was."""
    complexes_by_id = Complex.load_all(COMPLEXES)
    past_end = len(complexes_by_id) + 1
    with pytest.raises(MissingComplexError, match=f"complex {past_end} not found"):
        resolve_pairs([(1, past_end, 100.0)], complexes_by_id, COMPLEXES)
