from pathlib import Path

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.track_ridership import riders_on_stretch

SAS_PHASE_1 = ["R14", "B08", "Q03", "Q04", "Q05"]


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


def test_riders_between_consecutive_stops_on_the_stretch(tmp_path: Path) -> None:
    paths = tmp_path / "paths.parquet"
    write_paths(
        paths,
        [
            # Through the 57 St-63 St connector only, boarding and alighting off it.
            ("Q R16>R14>B08 | walk B08>B08", 1.0),
            # Several segments of the stretch: counted once.
            ("Q Q05>Q04>Q03>B08>R14>R16", 2.0),
            # The second ride is on the stretch.
            ("6 629>628 | walk 628>B08 | Q B08>Q03", 4.0),
            # Stops at Lexington Av/63 St on the 63 St line: not on the stretch.
            ("F B06>B08>B10", 8.0),
            # Walks between stretch stops aren't rides.
            ("walk Q03>Q04 | 6 628>627", 16.0),
            # Two of the stretch's stops, but not consecutive on this ride.
            ("N R14>R13>B08", 32.0),
        ],
    )
    assert riders_on_stretch(paths, SAS_PHASE_1) == 7.0
