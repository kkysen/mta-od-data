from pathlib import Path

from mta_od_data.analyze.common import connection
from mta_od_data.ridership.compute import Hop, line_hops_table, route_groups_table
from mta_od_data.ridership.trips import (
    crowded_trains,
    line_hours,
    load_trip_stops,
    place_hours,
    platform_loads,
)

SAS = [Hop("SAS", "R14", "B08"), Hop("SAS", "B08", "Q03")]


def write_dates(tmp_path: Path, dates: list[tuple[str, int, str]]) -> Path:
    """A manifest of `(date, days, trip rows)` dates, each its own trips file:
    `trip,route,stop,departure,on,off,load` rows, `;`-separated."""
    manifest = tmp_path / "manifest.csv"
    lines = ["date,days,trips"]
    for day, days, rows in dates:
        file = tmp_path / f"trips-{day}.parquet"
        values = ", ".join(
            f"('{t}', '{r}', 0, 0, {i}, '{s}', {d}, {d}, {on}, {off}, {load})"
            for i, row in enumerate(rows.split(";"))
            for t, r, s, d, on, off, load in [row.split(",")]
        )
        connection().execute(
            f"COPY (SELECT * FROM (VALUES {values}) t(trip_id, route_id, direction_id, "
            "day, stop_sequence, stop_id, arrival, departure, boardings, alightings, "
            f"load)) TO '{file}' (FORMAT parquet)"
        )
        lines.append(f"{day},{days},{file.name}")
    manifest.write_text("\n".join(lines) + "\n")
    return manifest


def test_trains_average_over_the_weekdays_they_run(tmp_path: Path) -> None:
    # A Q from 72 St through 63 St to 57 St, boarding at 72 St and 63 St:
    # 10 and 5 on a date standing for 3 weekdays, 2 and 5 on one for 1.
    busy = "a,Q,Q03,28800,10,0,10;a,Q,B08,28860,5,0,15;a,Q,R14,28920,0,15,0"
    quiet = "a,Q,Q03,28800,2,0,2;a,Q,B08,28860,5,0,7;a,Q,R14,28920,0,7,0"
    manifest = write_dates(
        tmp_path, [("2025-09-17", 3, busy), ("2025-09-18", 1, quiet)]
    )
    days = load_trip_stops(manifest, None).days
    assert days == 4
    route_groups_table({"Q": ["Q"]})
    # 63 St's platform leaving for 57 St.
    connection().execute(
        "CREATE OR REPLACE TEMP TABLE directions AS SELECT * FROM (VALUES "
        "('Q', 'B08', 'R14', 'S', 'S', 'p63', 'p57')) t(route, a, b, da, db, pa, pb)"
    )
    # Joining SAS: 10 + 5 on one date, 2 + 5 on the other, averaged over 4 weekdays.
    line_hops_table(SAS)
    assert line_hours(False, days) == [("SAS", 8, (15 * 3 + 7 * 1) / 4)]
    (train,) = crowded_trains(["Q"], 1)
    assert (train.peak, train.peak_stop, train.peak_next, train.days) == (
        (15 * 3 + 7 * 1) / 4,
        "B08",
        "R14",
        4,
    )
    # On and off at 63 St, at 08:00.
    hours = {(s, p, h): r for s, _, p, h, r in place_hours(False, days)}
    assert hours["B08", "p63", 8] == 5.0
    # 57 St's platform, by the segment arriving there.
    assert hours["R14", "p57", 8] == (15 * 3 + 7 * 1) / 4


def test_crowded_trains_peak_on_their_routes_usual_line(tmp_path: Path) -> None:
    # Twenty Rs from 59 St to 57 St, and two fuller Rs on to 63 St,
    # which too few Rs stop at to be on the R's usual line:
    # one fullest on to 63 St, so not counted,
    # and one fullest before, so counted.
    usual = ";".join(
        f"r{i},R,R11,{28800 + 600 * i},10,0,10;r{i},R,R14,{28860 + 600 * i},0,10,0"
        for i in range(20)
    )
    off = "x,R,R11,36000,20,0,20;x,R,R14,36060,30,0,50;x,R,B08,36120,0,50,0"
    on = "y,R,R11,37000,30,0,30;y,R,R14,37060,0,10,20;y,R,B08,37120,0,20,0"
    manifest = write_dates(tmp_path, [("2025-09-17", 1, f"{usual};{off};{on}")])
    load_trip_stops(manifest, None)
    (train,) = crowded_trains(["R"], 1)
    assert (train.peak, train.peak_stop) == (30, "R11")


def test_platform_loads_count_waiting_and_getting_off(tmp_path: Path) -> None:
    # A Q from 63 St to 57 St at 08:01, 15 getting off at 57 St at 08:02.
    trips = "a,Q,B08,28860,15,0,15;a,Q,R14,28920,0,15,0"
    manifest = write_dates(tmp_path, [("2025-09-17", 2, trips)])
    # 63 St's riders waiting for it, rising to 15 by 08:00.
    connection().execute(
        f"COPY (SELECT * FROM (VALUES ('Q', 0, 'B08', 'R14', 479, 7.5), "
        f"('Q', 0, 'B08', 'R14', 480, 15.0)) "
        "t(route_id, direction_id, stop_id, next_stop, minute, riders)) "
        f"TO '{tmp_path / 'platform-waits-2025-09-17.parquet'}' (FORMAT parquet)"
    )
    days = load_trip_stops(manifest, None).days
    route_groups_table({"Q": ["Q"]})
    connection().execute(
        "CREATE OR REPLACE TEMP TABLE directions AS SELECT * FROM (VALUES "
        "('Q', 'B08', 'R14', 'N', 'N', 'p63', 'p57')) t(route, a, b, da, db, pa, pb)"
    )
    loads = {p: (m, r) for _, _, p, m, r in platform_loads(manifest, None, days)}
    assert loads == {"p63": (480, 15.0), "p57": (482, 15.0)}
