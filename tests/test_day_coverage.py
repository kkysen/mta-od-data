"""`DayCoverage.query` is remembered per extract, and only per extract.

Its answer is a property of a file that a command reads before it reads
anything else, so several commands in one process share one scan of it.
Which makes the key the thing worth testing: a file whose contents have
changed under the same name has to be scanned again.
"""

from pathlib import Path

import duckdb
import pytest

from mta_od_data.analyze.common import DayCoverage, DayFilterError

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKDAY_FILTER = '"Day of Week" IN (?, ?, ?, ?, ?)'


def write_extract(path: Path, rows: list[tuple[int, int, str]]) -> Path:
    """A parquet with just the columns a coverage query reads."""
    values = ", ".join(f"({year}, {month}, '{day}')" for year, month, day in rows)
    duckdb.connect().execute(
        f"""
        COPY (
            SELECT * FROM (VALUES {values})
            AS t("Year", "Month", "Day of Week")
        ) TO '{path}' (FORMAT PARQUET)
        """
    )
    return path


@pytest.fixture
def extract(tmp_path: Path) -> Path:
    return write_extract(
        tmp_path / "extract.parquet",
        [(2025, 1, day) for day in [*WEEKDAYS, "Saturday"]],
    )


def test_coverage_counts_month_and_day_groups(extract: Path) -> None:
    coverage = DayCoverage.query(extract, WEEKDAY_FILTER, WEEKDAYS)
    assert coverage == DayCoverage(
        n_days=5, first_month="2025-01", last_month="2025-01"
    )


def test_the_same_extract_and_filter_is_queried_once(extract: Path) -> None:
    # Identity, not equality: two equal `DayCoverage`s would also be two
    # scans of a 358MB file, which is the whole point of the cache.
    assert DayCoverage.query(extract, WEEKDAY_FILTER, WEEKDAYS) is DayCoverage.query(
        extract, WEEKDAY_FILTER, WEEKDAYS
    )


def test_a_rewritten_extract_is_queried_again(extract: Path) -> None:
    """`prepare` writing a new extract to the same path,
    which a key of the path alone would go on answering for."""
    before = DayCoverage.query(extract, WEEKDAY_FILTER, WEEKDAYS)
    write_extract(extract, [(2026, m, "Monday") for m in (1, 2, 3)])
    after = DayCoverage.query(extract, WEEKDAY_FILTER, WEEKDAYS)
    assert (before.n_days, before.last_month) == (5, "2025-01")
    assert (after.n_days, after.last_month) == (3, "2026-03")


def test_a_filter_matching_nothing_says_so(extract: Path) -> None:
    """And says so every time, the error not being what's remembered."""
    for _ in range(2):
        with pytest.raises(DayFilterError, match="Sunday"):
            DayCoverage.query(extract, '"Day of Week" IN (?)', ["Sunday"])
