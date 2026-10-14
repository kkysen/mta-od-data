"""Riders on each train, from `mta-od-data raptor assign-range`'s per-date trips files.

Each date's file has every train's riders boarding and alighting at each of its stops,
and on board as it leaves, as routed (`raptor/raptor_design.md`).
Here they're weighted by each date's `days`, as paths are,
and with fare evaders, by the evasion rate in the quarter of the date the train is on:
a train past midnight (24:00 or later on the service day's clock) is on the next date.

A train on one date is the same as one on another
with the same route, direction, departure from its first stop, and stops,
whatever its trip ID: IDs change between feed versions.
Its stops too, as planned work can reroute a train that leaves when it always does
(the F via 53 St, not 63 St).
"""

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.path_riders import FareEvasion, read_manifest

# NYCT's GTFS: direction 0 is northbound, its stops' `N` platforms.
DIRECTIONS = {0: "N", 1: "S"}

DAY = 24 * 60 * 60

# What `trip_stops` was last loaded from, so a run of reports loads it once.
_loaded: dict[str, object] = {}


@dataclass(frozen=True, slots=True)
class TripStops:
    """`load_trip_stops`' table's dates' weekdays: what its riders average over."""

    days: int


def load_trip_stops(manifest: Path, evasion: FareEvasion | None) -> TripStops:
    """Every date's trains' stops as a temp table `trip_stops`:
    each row's date `d`, its `w`eight (`days`, times evasion's 1 / (1 - rate)),
    the train's key (route, direction, first stop, departure there, its stops),
    its `dir` (`N` or `S`), and the trips file's columns."""
    rows = read_manifest(manifest)
    days = sum(int(row["days"]) for row in rows)
    key = (
        manifest,
        None if evasion is None else (evasion.year, *evasion.rates.items()),
    )
    if _loaded.get("trip_stops") == key:
        return TripStops(days)

    def factor(day: date) -> float:
        return 1.0 if evasion is None else 1 / (1 - evasion.rate(day))

    parts = []
    for d, row in enumerate(rows):
        if not row.get("trips"):
            raise ValueError(
                f"{manifest}: no trips files; rerun `mta-od-data raptor assign-range`"
            )
        file = manifest.parent / Path(row["trips"]).name
        day = date.fromisoformat(row["date"])
        today, tomorrow = factor(day), factor(day + timedelta(days=1))
        parts.append(
            f"SELECT {d} AS d, {int(row['days'])} AS days, "
            f"{int(row['days'])} * if(departure < {DAY}, {today}, {tomorrow}) AS w, * "
            f"FROM read_parquet('{file}')"
        )
    directions = ", ".join(f"({k}, '{v}')" for k, v in DIRECTIONS.items())
    connection().execute(
        f"""
        CREATE OR REPLACE TEMP TABLE trip_stops AS
        SELECT s.*, dirs.dir,
            first_value(stop_id) OVER t AS first_stop,
            first_value(departure) OVER t AS first_departure,
            string_agg(stop_id, ' ') OVER (
                PARTITION BY d, trip_id, day ORDER BY stop_sequence
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ) AS stops,
            lag(stop_id) OVER t AS prev_stop,
            lead(stop_id) OVER t AS next_stop
        FROM ({" UNION ALL ".join(parts)}) s
        LEFT JOIN (VALUES {directions}) dirs(direction_id, dir) USING (direction_id)
        WINDOW t AS (PARTITION BY d, trip_id, day ORDER BY stop_sequence)
        """
    )
    _loaded["trip_stops"] = key
    return TripStops(days)


def place_hours(with_route: bool, days: int) -> list[tuple[Any, ...]]:
    """Riders on and off each stop's trains (each of `route_groups`' routes'),
    by stop, direction, (route,) and the hour the train is there:
    `(stop, dir, [route,] hour, riders)` rows, an average weekday's."""
    grp = ", grp" if with_route else ""
    return (
        connection()
        .execute(
            f"""
            SELECT stop_id, dir{grp}, departure // 3600 AS hour,
                sum((boardings + alightings) * w) / {days}
            FROM trip_stops JOIN route_groups ON route = route_id
            WHERE route_id IN (SELECT route FROM route_groups)
            GROUP BY ALL
            """
            if with_route
            else f"""
            SELECT stop_id, dir, departure // 3600 AS hour,
                sum((boardings + alightings) * w) / {days}
            FROM trip_stops
            WHERE route_id IN (SELECT route FROM route_groups)
            GROUP BY ALL
            """
        )
        .fetchall()
    )


def route_hours(days: int) -> list[tuple[Any, ...]]:
    """Riders boarding each `route_groups` row's trains, by the hour they board:
    `(route, hour, riders)` rows."""
    return (
        connection()
        .execute(
            f"""
            SELECT grp, departure // 3600 AS hour, sum(boardings * w) / {days}
            FROM trip_stops JOIN route_groups ON route = route_id
            GROUP BY ALL
            """
        )
        .fetchall()
    )


def line_hours(
    lines: list[dict[str, object]], with_route: bool, days: int
) -> list[tuple[Any, ...]]:
    """Riders joining each line's track on its trains, by the hour they join:
    `(line, [route,] hour, riders)` rows.

    At a stop whose next segment is on the line, riders join it by boarding there,
    and if the segment before isn't on the line, so do all those staying on."""
    grp = ", grp" if with_route else ""
    return (
        connection()
        .execute(
            f"""
            WITH s AS (
                SELECT l.name, route_id, departure, w, boardings, load,
                    list_contains(l.stops, stop_id)
                        AND list_contains(l.stops, next_stop) AS on_out,
                    list_contains(l.stops, stop_id)
                        AND coalesce(list_contains(l.stops, prev_stop), false) AS on_in
                FROM trip_stops, (SELECT unnest($lines) AS l)
                WHERE route_id IN (SELECT route FROM route_groups)
            )
            SELECT name{grp}, departure // 3600 AS hour,
                sum(if(on_in, boardings, load) * w) / {days}
            FROM s {"JOIN route_groups ON route = route_id" if with_route else ""}
            WHERE on_out
            GROUP BY ALL
            """,
            {"lines": lines},
        )
        .fetchall()
    )


@dataclass(frozen=True, slots=True)
class Train:
    """A train's average load at its busiest, over the weekdays it runs."""

    route: str
    first_stop: str
    first_departure: int
    last_stop: str
    peak: float
    # Where its load peaks: leaving `peak_stop` for `peak_next`, at `peak_departure`.
    peak_stop: str
    peak_next: str
    peak_departure: int
    days: int


def crowded_trains(routes: Sequence[str], top: int) -> list[Train]:
    """Each of `routes`' `top` trains by their average peak load, busiest first."""
    rows = (
        connection()
        .execute(
            """
            WITH trains AS (
                -- Its stop and next are its key's `stops`'; departures, the earliest.
                SELECT route_id, direction_id, first_stop, first_departure, stops,
                    stop_sequence, stop_id, next_stop, min(departure) AS departure,
                    sum(load * w) / sum(days) AS load, sum(days) AS days
                FROM trip_stops
                WHERE route_id IN (SELECT unnest($routes))
                GROUP BY ALL
            ),
            peaks AS (
                SELECT *,
                    max(load) OVER k AS peak,
                    last_value(stop_id) OVER (
                        k ORDER BY stop_sequence
                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                    ) AS last_stop
                FROM trains
                WINDOW k AS (
                    PARTITION BY
                        route_id, direction_id, first_stop, first_departure, stops
                )
                -- Where it peaks: its first stop with its greatest load.
                QUALIFY row_number() OVER (k ORDER BY load DESC, stop_sequence) = 1
            )
            SELECT route_id, first_stop, first_departure, last_stop, peak,
                stop_id, coalesce(next_stop, ''), departure, days
            FROM peaks
            QUALIFY row_number() OVER (
                PARTITION BY route_id
                ORDER BY round(peak) DESC, first_departure, first_stop, stops
            ) <= $top
            ORDER BY round(peak) DESC, route_id, first_departure, stops
            """,
            {"routes": list(routes), "top": top},
        )
        .fetchall()
    )
    return [Train(*row) for row in rows]
