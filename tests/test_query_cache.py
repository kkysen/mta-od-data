"""`cached_rows` serves a query's rows again
only for the same query on the same files."""

from pathlib import Path

import pytest

from mta_od_data.analyze import common
from mta_od_data.analyze.common import cached_rows, connection

QUERY = "SELECT sum(x) FROM read_parquet(?)"


def write(path: Path, values: list[int]) -> None:
    rows = ", ".join(f"({v})" for v in values)
    connection().execute(
        f"COPY (SELECT * FROM (VALUES {rows}) t(x)) TO '{path}' (FORMAT parquet)"
    )


@pytest.fixture
def parquet(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(common, "QUERIES", tmp_path / "queries")
    path = tmp_path / "x.parquet"
    write(path, [1, 2])
    return path


def test_cached(parquet: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert cached_rows(QUERY, [str(parquet)], [parquet]) == [(3,)]

    def no_query() -> None:
        raise AssertionError("queried again")

    monkeypatch.setattr(common, "connection", no_query)
    assert cached_rows(QUERY, [str(parquet)], [parquet]) == [(3,)]


def test_rewritten_file_misses(parquet: Path) -> None:
    assert cached_rows(QUERY, [str(parquet)], [parquet]) == [(3,)]
    write(parquet, [10, 20, 30])
    assert cached_rows(QUERY, [str(parquet)], [parquet]) == [(60,)]


def test_other_query_misses(parquet: Path) -> None:
    assert cached_rows(QUERY, [str(parquet)], [parquet]) == [(3,)]
    other = "SELECT max(x) FROM read_parquet(?)"
    assert cached_rows(other, [str(parquet)], [parquet]) == [(2,)]
