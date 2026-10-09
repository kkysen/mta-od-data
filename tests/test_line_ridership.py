from pathlib import Path

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.line_ridership import (
    Pattern,
    riders_by_group,
    route_length,
    segment_lengths,
)


def write_paths(path: Path, rows: list[tuple[str, float]]) -> None:
    values = ", ".join(f"({i}, '{p}', {r})" for i, (p, r) in enumerate(rows))
    connection().execute(
        f"""
        COPY (
            SELECT 8 AS hour, i AS origin, 0 AS destination, path, riders
            FROM (VALUES {values}) t(i, path, riders)
        ) TO '{path}' (FORMAT parquet)
        """
    )


def test_riders_once_per_group(tmp_path: Path) -> None:
    paths = tmp_path / "paths.parquet"
    write_paths(
        paths,
        [
            # Two rides on one group: counted once.
            ("2 120>127 | 3 127>132", 1.0),
            # One ride on each of two groups.
            ("7 701>702 | walk 702>703 | E 703>704", 2.0),
            # Walks aren't rides.
            ("walk 127>R16", 4.0),
            # Routes outside every group don't count.
            ("SI S31>S30", 8.0),
        ],
    )
    groups = {"2": "7 Av", "3": "7 Av", "7": "Flushing", "E": "8 Av"}
    assert riders_by_group(paths, groups) == {"7 Av": 1.0, "Flushing": 2.0, "8 Av": 2.0}


def pattern(route: str, stops: str, lengths: list[float]) -> Pattern:
    return Pattern(route, "Weekday", tuple(stops.split()), tuple(lengths))


def test_route_length_counts_regular_local_track_once() -> None:
    local = pattern("6", "a b c d", [1.0, 1.0, 1.0])
    # Express over the local's track: skips `b` and `c`, so adds nothing.
    express = pattern("6X", "a d e", [2.5, 4.0])
    # A rare extension: under `REGULAR_SHARE` of the 6's trips.
    extension = pattern("6", "a b c d f", [1.0, 1.0, 1.0, 8.0])
    patterns = {local: 95, express: 50, extension: 5}
    lengths = segment_lengths(patterns)
    assert route_length(patterns, lengths) == 3.0 + 4.0
