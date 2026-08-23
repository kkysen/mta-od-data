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


def test_loading_twice_yields_the_same_objects() -> None:
    """A run loads each file once, but nothing enforces that, and a
    second load handing back equal-but-distinct objects would make
    every `==` and every dict lookup on them silently wrong."""
    complexes_by_id = Complex.load_all(COMPLEXES)
    again = Complex.load_all(COMPLEXES)
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
