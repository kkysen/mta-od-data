"""The `ridership` reports' rows, from `mta-od-data raptor assign-range`'s paths
and trips, before they're named and laid out as tables (`__init__.py`).

Everything here is what a report's numbers depend on, so `cache.py` keys its
cached rows on this module's source, and `trips.py`'s and `service.py`'s:
a report's wording, or its places' names, can change without recomputing them.
"""

from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Any

import json5
from typer import BadParameter

from mta_od_data.analyze.common import connection
from mta_od_data.analyze.path_riders import (
    AveragePaths,
    average_path_riders,
    counting,
    load_fare_evasion,
    read_manifest,
)
from mta_od_data.gtfs import DEFAULT_GTFS_DIR
from mta_od_data.ridership.service import (
    Pattern,
    load_feed,
    route_length,
    segment_lengths,
)
from mta_od_data.ridership.trips import (
    DAY,
    Train,
    crowded_trains,
    hop_on,
    line_hours,
    load_trip_stops,
    place_hours,
    route_hours,
)

HERE = Path(__file__).parent

TRAIN_LENGTHS = HERE / "train_lengths.json5"
# Loads per this much train: a B Division car's length, most cars',
# so a load per car compares across trains of different cars.
CAR_FT = 60
# Each route's stops' physical platforms, from OpenStreetMap (`platforms.py`).
PLATFORMS = HERE / "platforms.csv"


def load_train_lengths(path: Path = TRAIN_LENGTHS) -> dict[str, int]:
    """Each GTFS route's train length, in feet."""
    lengths = json5.loads(path.read_text(), allow_duplicate_keys=False)
    return {route: int(feet) for route, feet in lengths.items()}


class By(StrEnum):
    COMPLEX = "complex"
    STATION = "station"
    STATION_DIRECTION = "station-direction"
    PLATFORM = "platform"
    ROUTE = "route"
    LINE = "line"
    TRIP = "trip"


PLACES = frozenset({By.COMPLEX, By.STATION, By.STATION_DIRECTION, By.PLATFORM})

# Express variants the feed lists as routes of their own, and their routes.
VARIANTS = {"5X": "5", "6X": "6", "7X": "7", "FX": "F"}

# Routes in the feed but not the OD data, which is subway only.
NOT_IN_OD = frozenset({"SI"})


def route_groups(route: str, routes: Iterable[str]) -> list[str]:
    """The `--by route` rows a GTFS route's rides count towards,
    of all `routes`' (a route has a local row only beside its express variant's)."""
    if route in NOT_IN_OD:
        return []
    if (base := VARIANTS.get(route)) is not None:
        return [base, route]
    if any(VARIANTS.get(r) == route for r in routes):
        return [route, f"{route}L"]
    return [route]


def base_route(group: str) -> str:
    """The route a `--by route` row is a variant of, or itself."""
    if group.endswith("L") and group[:-1] in VARIANTS.values():
        return group[:-1]
    return VARIANTS.get(group, group)


@dataclass(frozen=True, slots=True)
class Column:
    """One way of counting riders, and each path's average under it."""

    label: str
    average: AveragePaths
    # The year its OD data is scaled to the counted entries of, if scaled.
    scaled_to: int | None = None


def period(manifest: Path) -> str:
    """The manifest's dates as a column name, e.g. "Aug-Dec 2025"."""
    days = sorted(date.fromisoformat(row["date"]) for row in read_manifest(manifest))
    first, last = days[0], days[-1]
    if first.year != last.year:
        return f"{first:%b %Y}-{last:%b %Y}"
    if first.month != last.month:
        return f"{first:%b}-{last:%b %Y}"
    return f"{first:%b %Y}"


def columns(
    manifest: Path, od_factors: Sequence[Path], fare_evasion: bool, unscaled: bool
) -> list[Column]:
    # One at a time: `counting` loads its factors into the tables
    # `average_path_riders` reads, so each is averaged before the next loads.
    cols: list[Column] = []
    if unscaled:
        c = counting(None, fare_evasion)
        cols.append(Column(period(manifest), average_path_riders(manifest, c)))
    for factors in od_factors:
        c = counting(factors, fare_evasion)
        assert c.scale is not None, "counting with factors scales"
        year = c.scale.year
        cols.append(Column(str(year), average_path_riders(manifest, c), year))
    days = {col.average.days for col in cols}
    assert len(days) == 1, f"one manifest, one number of days: {days}"
    return cols


# What each temp table was last built from, so a process running several reports
# (the snapshot tests) builds each once: `legs` takes ~3 s, `events` ~5 s,
# and `directions` reads every feed, ~8 s.
built: dict[str, object] = {}


def load_legs(cols: Sequence[Column]) -> list[str]:
    """Each path's legs as a temp table `legs`,
    with each column's riders as `r0`, `r1`, and so on; returns those names.

    `route` is the leg's route, or `walk`, and `stops` its parent stops in order.
    """
    db = connection()
    names = [f"r{k}" for k in range(len(cols))]
    files = [str(col.average.file) for col in cols]
    if built.get("legs") == files:
        return names
    built.pop("events", None)
    union = " UNION ".join(f"SELECT path FROM read_parquet('{f}')" for f in files)
    joins = " ".join(
        f"LEFT JOIN read_parquet('{f}') c{k} USING (path)" for k, f in enumerate(files)
    )
    riders = ", ".join(f"coalesce(c{k}.riders, 0) AS {n}" for k, n in enumerate(names))
    db.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE legs AS
        SELECT
            path, {", ".join(names)}, i,
            split_part(leg, ' ', 1) AS route,
            string_split(split_part(leg, ' ', 2), '>') AS stops
        FROM (
            SELECT
                path, {", ".join(names)},
                unnest(string_split(path, ' | ')) AS leg,
                unnest(range(1, len(string_split(path, ' | ')) + 1)) AS i
            FROM (SELECT p.path, {riders} FROM ({union}) p {joins})
        )
        """
    )
    built["legs"] = files
    return names


def ride_routes(routes: Sequence[str]) -> tuple[list[str], dict[str, list[str]]]:
    """The GTFS routes of `legs`' rides that `--route` keeps (all, if none),
    and each one's `--by route` rows."""
    every = [
        r
        for (r,) in connection()
        .execute("SELECT DISTINCT route FROM legs WHERE route != 'walk'")
        .fetchall()
    ]
    groups = {r: gs for r in every if (gs := route_groups(r, every))}
    if routes:
        known = set().union(*groups.values())
        if unknown := sorted(set(routes) - known):
            raise BadParameter(
                f"no rides on {', '.join(unknown)}", param_hint="--route"
            )
        groups = {r: gs for r, gs in groups.items() if set(gs) & set(routes)}
    return sorted(groups), groups


def route_groups_table(groups: dict[str, list[str]]) -> None:
    connection().execute(
        "CREATE OR REPLACE TEMP TABLE route_groups AS "
        "SELECT unnest($routes) AS route, unnest($groups) AS grp",
        {
            "routes": [r for r, gs in groups.items() for _ in gs],
            "groups": [g for gs in groups.values() for g in gs],
        },
    )


def directions_table(manifest: Path) -> None:
    """Each route's consecutive stops' platform directions, from every date's feed,
    and their physical platforms (`platforms.csv`, `mta-od-data fetch-platforms`'s),
    as a temp table `directions`: `route`, `a`, `b`, `da`, `db`, `pa`, `pb`."""
    if built.get("directions") == manifest:
        return
    directions: dict[tuple[str, str, str], tuple[str, str]] = {}
    for row in read_manifest(manifest):
        directions |= load_feed(DEFAULT_GTFS_DIR / Path(row["feed"]).name).directions
    keys = list(directions)
    connection().execute(
        f"""
        CREATE OR REPLACE TEMP TABLE directions AS
        SELECT d.*,
            coalesce(p.stop_platform, '') AS pa, coalesce(p.next_platform, '') AS pb
        FROM (
            SELECT unnest($route) AS route, unnest($a) AS a, unnest($b) AS b,
                unnest($da) AS da, unnest($db) AS db
        ) d
        LEFT JOIN read_csv('{PLATFORMS}', all_varchar = true) p
            ON p.route = d.route AND p.stop = d.a AND p.next_stop = d.b
        """,
        {
            "route": [k[0] for k in keys],
            "a": [k[1] for k in keys],
            "b": [k[2] for k in keys],
            "da": [directions[k][0] for k in keys],
            "db": [directions[k][1] for k in keys],
        },
    )
    built["directions"] = manifest


def build_events(routes: Sequence[str], names: list[str], merge: bool) -> None:
    """Each ride's boarding and alighting on `routes` as a temp table `events`:
    its stop, platform direction, route, riders per column,
    and whether it's a boarding and a transfer;
    and the first column's riders staying on at each stop between, as `staying`,
    by stop, platform direction, and route.
    With `merge`, consecutive rides on `routes` changing at a stop are one ride,
    staying on there.

    A ride lists only the stops its train stops at (an express skips the locals),
    so riders staying on are those on a train stopping there."""
    key = (built.get("legs"), tuple(routes), merge)
    if built.get("events") == key:
        return
    db = connection()
    db.execute(
        """
        CREATE OR REPLACE TEMP TABLE rides AS
        WITH l AS (
            SELECT *, route IN $routes AS f FROM legs
        ),
        -- Over every leg, then only `routes`' rides kept:
        -- a journey's first and last rides, and the legs beside one, may be off them.
        w AS (
            SELECT *,
                $merge AND f AND coalesce(lag(f) OVER p, false)
                    AND lag(stops[-1]) OVER p = stops[1] AS cont_in,
                $merge AND f AND coalesce(lead(f) OVER p, false)
                    AND lead(stops[1]) OVER p = stops[-1] AS cont_out,
                min(if(route != 'walk', i, NULL)) OVER (PARTITION BY path)
                    AS first_ride,
                max(if(route != 'walk', i, NULL)) OVER (PARTITION BY path)
                    AS last_ride
            FROM l
            WINDOW p AS (PARTITION BY path ORDER BY i)
        )
        SELECT * FROM w WHERE f
        """,
        {"routes": list(routes), "merge": merge},
    )
    db.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE events AS
        SELECT w.path, stops[1] AS stop, coalesce(d.da, '') AS dir,
            coalesce(d.pa, '') AS platform, w.route,
            {", ".join(names)}, true AS boarding, i > first_ride AS transfer
        FROM rides w
        LEFT JOIN directions d
            ON d.route = w.route AND d.a = stops[1] AND d.b = stops[2]
        WHERE NOT cont_in
        UNION ALL
        SELECT w.path, stops[-1], coalesce(d.db, ''), coalesce(d.pb, ''), w.route,
            {", ".join(names)}, false, i < last_ride
        FROM rides w
        LEFT JOIN directions d
            ON d.route = w.route AND d.a = stops[-2] AND d.b = stops[-1]
        WHERE NOT cont_out
        """
    )
    first = names[0]
    db.execute(
        f"""
        CREATE OR REPLACE TEMP TABLE staying AS
        WITH between AS (
            SELECT route, stops, {first}, unnest(range(2, len(stops))) AS j
            FROM rides
        )
        SELECT stops[j] AS stop, coalesce(d.da, '') AS dir,
            coalesce(d.pa, '') AS platform, b.route, sum({first}) AS riders
        FROM between b
        LEFT JOIN directions d
            ON d.route = b.route AND d.a = stops[j] AND d.b = stops[j + 1]
        GROUP BY ALL
        UNION ALL
        SELECT stops[-1], coalesce(d.db, ''), coalesce(d.pb, ''), w.route,
            sum({first})
        FROM rides w
        LEFT JOIN directions d
            ON d.route = w.route AND d.a = stops[-2] AND d.b = stops[-1]
        WHERE cont_out
        GROUP BY ALL
        """
    )
    db.execute("DROP TABLE rides")
    built["events"] = key


def place_rows(with_route: bool, names: list[str]) -> list[tuple[Any, ...]]:
    """`events` by stop, direction, platform (and route): riders on and off per column,
    then the first column's boardings, alightings, transfers on and off,
    and riders staying on."""
    grp = ", grp" if with_route else ""
    join_route = "JOIN route_groups USING (route)" if with_route else ""
    first = names[0]
    sums = ", ".join(f"sum({n})::DOUBLE AS {n}" for n in names)
    values = ", ".join(
        f"coalesce({v}, 0)" for v in [*names, "boarded", "alighted", "transfers"]
    )
    return (
        connection()
        .execute(
            f"""
            WITH e AS (
                SELECT stop, dir, platform{grp}, {sums},
                    sum({first}) FILTER (WHERE boarding)::DOUBLE AS boarded,
                    sum({first}) FILTER (WHERE NOT boarding)::DOUBLE AS alighted,
                    sum({first}) FILTER (WHERE transfer)::DOUBLE AS transfers
                FROM events {join_route}
                GROUP BY ALL
            ),
            s AS (
                SELECT stop, dir, platform{grp}, sum(riders)::DOUBLE AS staying
                FROM staying {join_route}
                GROUP BY ALL
            )
            -- Full, for stops riders only stay on at.
            SELECT stop, dir, platform{grp}, {values}, coalesce(staying, 0)
            FROM e FULL JOIN s USING (stop, dir, platform{grp})
            """
        )
        .fetchall()
    )


@dataclass(slots=True)
class RouteService:
    """A `--by route` row's average route km, trips, and train-km,
    and car-km: train-km times its trains' lengths in 60-ft cars' worth."""

    route_km: float = 0.0
    trips: float = 0.0
    train_km: float = 0.0
    car_km: float = 0.0


def route_service(
    manifest: Path, groups: dict[str, list[str]]
) -> dict[str, RouteService]:
    """Each `--by route` row's route km, trips, and train-km,
    from each date's feed, averaged as its riders are."""
    totals: defaultdict[str, RouteService] = defaultdict(RouteService)
    total_days = 0
    train_lengths = load_train_lengths()
    for row in read_manifest(manifest):
        feed = load_feed(DEFAULT_GTFS_DIR / Path(row["feed"]).name)
        days = int(row["days"])
        total_days += days
        patterns = feed.patterns_on(date.fromisoformat(row["date"]))
        lengths = segment_lengths(patterns)
        by_group: defaultdict[str, dict[Pattern, int]] = defaultdict(dict)
        for p, n in patterns.items():
            for g in groups.get(p.route, []):
                by_group[g][p] = n
        for g, ps in by_group.items():
            t = totals[g]
            t.route_km += route_length(ps, lengths) / 1000 * days
            t.trips += sum(ps.values()) * days
            t.train_km += sum(n * sum(p.lengths) for p, n in ps.items()) / 1000 * days
            t.car_km += (
                sum(
                    n * sum(p.lengths) * train_lengths.get(p.route, 0) / CAR_FT
                    for p, n in ps.items()
                )
                / 1000
                * days
            )
    return {
        g: RouteService(
            t.route_km / total_days,
            t.trips / total_days,
            t.train_km / total_days,
            t.car_km / total_days,
        )
        for g, t in totals.items()
    }


def route_rows(names: list[str], with_line: bool) -> list[tuple[Any, ...]]:
    line = ", name" if with_line else ""
    on_line = "JOIN leg_lines USING (route, stops)" if with_line else ""
    sums = ", ".join(f"sum({n})::DOUBLE" for n in names)
    return (
        connection()
        .execute(
            f"""
            WITH {LEG_LINES if with_line else "x AS (SELECT 1)"},
            journeys AS (
                SELECT DISTINCT path, grp{line}, {", ".join(names)}
                FROM legs JOIN route_groups USING (route) {on_line}
            )
            SELECT grp{line}, {sums} FROM journeys GROUP BY ALL
            """,
        )
        .fetchall()
    )


# The lines each ride rides, by its route and stops:
# matched once for each different ride, however many paths take it.
LEG_LINES = f"""
    leg_lines AS (
        SELECT DISTINCT route, stops, name
        FROM (
            SELECT route, stops, unnest(stops[:-2]) AS a, unnest(stops[2:]) AS b
            FROM (
                SELECT DISTINCT route, stops FROM legs
                WHERE route IN (SELECT route FROM route_groups)
            )
        ) h
        JOIN line_hops USING (a, b)
        WHERE {hop_on("line_hops", "route")}
    )
"""


@dataclass(frozen=True, slots=True)
class Hop:
    """A line's track between two stops a train stops at one after the other,
    either way: on only `routes`' trains, if any, and never on `not_routes`'."""

    line: str
    a: str
    b: str
    routes: tuple[str, ...] = ()
    not_routes: tuple[str, ...] = ()


def pairs(seqs: Iterable[Sequence[str]]) -> list[tuple[str, str]]:
    return [(s[k], s[k + 1]) for s in seqs for k in range(len(s) - 1)]


def track_hops(name: str, tracks: Iterable[Any]) -> list[Hop]:
    """A trunk's `tracks`: each a list of stops, or `{routes, stops}`
    for track only `routes`' trains ride, where another line's stops share its IDs."""
    hops: list[Hop] = []
    for t in tracks:
        stops, routes = (t["stops"], tuple(t["routes"])) if "stops" in t else (t, ())
        hops += [Hop(name, a, b, routes) for a, b in pairs([stops])]
    return hops


def trunk_hops(name: str, trunk: dict[str, Any]) -> list[Hop]:
    """A `lines.json5` trunk's hops, as the trunk and,
    if it has `express` stops, its local and express tracks."""
    local = pairs(trunk.get("local", []))
    express = pairs(trunk.get("express", []))
    routes = tuple(trunk.get("express_routes", []))
    hops = track_hops(name, trunk.get("tracks", []))
    hops += [Hop(name, a, b) for a, b in dict.fromkeys(local + express)]
    if not express:
        return hops
    both = {frozenset(h) for h in local} & {frozenset(h) for h in express}
    if both and not routes:
        raise ValueError(f"{name}: no `express_routes` to tell {sorted(both)} apart")
    for a, b in dict.fromkeys(local):
        shared = frozenset((a, b)) in both
        hops.append(Hop(f"{name} local", a, b, not_routes=routes if shared else ()))
    for a, b in dict.fromkeys(express):
        shared = frozenset((a, b)) in both
        hops.append(Hop(f"{name} express", a, b, routes=routes if shared else ()))
    return hops


def load_lines(path: Path) -> list[Hop]:
    lines = json5.loads(path.read_text(), allow_duplicate_keys=False)
    hops = [h for name, trunk in lines.items() for h in trunk_hops(name, trunk)]
    seen = set()
    for h in hops:
        if (key := (h.line, frozenset((h.a, h.b)))) in seen:
            raise ValueError(f"{path}: {h.line} lists {h.a} to {h.b} twice")
        seen.add(key)
    return hops


def line_hops_table(hops: list[Hop]) -> None:
    """`hops` as a temp table `line_hops`, each both ways."""
    both = [*hops, *(Hop(h.line, h.b, h.a, h.routes, h.not_routes) for h in hops)]
    connection().execute(
        "CREATE OR REPLACE TEMP TABLE line_hops AS "
        "SELECT unnest($names) AS name, unnest($a) AS a, unnest($b) AS b, "
        "unnest($routes)::VARCHAR[] AS routes, "
        "unnest($not_routes)::VARCHAR[] AS not_routes",
        {
            "names": [h.line for h in both],
            "a": [h.a for h in both],
            "b": [h.b for h in both],
            "routes": [list(h.routes) for h in both],
            "not_routes": [list(h.not_routes) for h in both],
        },
    )


def line_rows(names: list[str]) -> list[tuple[Any, ...]]:
    sums = ", ".join(f"sum({n})::DOUBLE" for n in names)
    return (
        connection()
        .execute(
            f"""
            WITH {LEG_LINES},
            journeys AS (
                SELECT DISTINCT path, name, {", ".join(names)}
                FROM legs JOIN leg_lines USING (route, stops)
            )
            SELECT name, {sums} FROM journeys GROUP BY ALL
            """
        )
        .fetchall()
    )


def platform_routes() -> list[tuple[Any, ...]]:
    """Each platform's stop, direction, and routes (from `trip_stops`):
    those with a tenth of their trains at the station by day, from 6 AM to 9 PM,
    there, or all its routes if none are there by day:
    `(platform, stop, dir, routes)` rows."""
    return (
        connection()
        .execute(
            f"""
            WITH s AS (
                SELECT coalesce(leaving.pa, arriving.pb, '') AS platform,
                    stop_id AS stop, coalesce(leaving.da, arriving.db) AS dir,
                    route_id AS route,
                    count(*) FILTER (
                        departure % {DAY} BETWEEN 6 * 3600 AND 21 * 3600
                    ) AS by_day
                FROM trip_stops t
                LEFT JOIN directions leaving
                    ON leaving.route = t.route_id AND leaving.a = t.stop_id
                    AND leaving.b = t.next_stop
                LEFT JOIN directions arriving
                    ON arriving.route = t.route_id AND arriving.a = t.prev_stop
                    AND arriving.b = t.stop_id
                GROUP BY ALL
            ),
            -- A route is by day at a platform with a tenth of its trains there.
            r AS (
                SELECT *,
                    by_day > 0
                    AND by_day >= 0.1 * sum(by_day) OVER (PARTITION BY stop, route)
                        AS kept
                FROM s
            )
            SELECT platform, stop, dir,
                if(bool_or(kept), list(route ORDER BY route) FILTER (kept),
                    list(route ORDER BY route))
            FROM r
            WHERE platform != ''
            GROUP BY ALL
            ORDER BY ALL
            """
        )
        .fetchall()
    )


@dataclass(frozen=True, slots=True)
class Computed:
    """A report's rows, as `compute` returns them, for `__init__.py` to lay out."""

    days: int
    cols: list[Column] = field(default_factory=list)
    # A place's, route's, or line's riders, by what `place_rows`, `route_rows`,
    # or `line_rows` total them by.
    rows: list[tuple[Any, ...]] = field(default_factory=list)
    # Their riders by the hour, by `place_hours`, `route_hours`, or `line_hours`.
    hours: list[tuple[Any, ...]] = field(default_factory=list)
    # `--by platform`: `platform_routes`.
    platforms: list[tuple[Any, ...]] = field(default_factory=list)
    # `--by route`: each row's service.
    service: dict[str, RouteService] = field(default_factory=dict)
    # `--by trip`: each route's most crowded trains.
    trains: list[Train] = field(default_factory=list)


def trip_routes(route: Sequence[str]) -> list[str]:
    """The GTFS routes of `trip_stops`' trains that `--route` keeps (all, if none)."""
    every = [
        r
        for (r,) in connection()
        .execute("SELECT DISTINCT route_id FROM trip_stops")
        .fetchall()
    ]
    groups = {r: gs for r in every if (gs := route_groups(r, every))}
    return sorted(r for r, gs in groups.items() if not route or set(gs) & set(route))


def compute(
    by: Sequence[By],
    route: Sequence[str],
    manifest: Path,
    od_factors: Sequence[Path],
    unscaled: bool,
    fare_evasion: bool,
    lines: Path,
    top: int,
) -> Computed:
    """A report's rows: `ridership`'s, once its `--by` is checked."""
    dims = set(by)
    evasion = load_fare_evasion(None) if fare_evasion else None
    if By.TRIP in dims:
        days = load_trip_stops(manifest, evasion).days
        return Computed(days, trains=crowded_trains(trip_routes(route), top))
    cols = columns(manifest, od_factors, fare_evasion, unscaled)
    names = load_legs(cols)
    kept, groups = ride_routes(route)
    route_groups_table(groups)
    with_route = By.ROUTE in dims and len(dims) > 1
    days = load_trip_stops(manifest, evasion).days
    if places := dims & PLACES:
        (place,) = places
        directions_table(manifest)
        build_events(kept, names, merge=bool(route) and not with_route)
        return Computed(
            days,
            cols,
            place_rows(with_route, names),
            place_hours(with_route, days),
            platform_routes() if place is By.PLATFORM else [],
        )
    if By.LINE in dims:
        line_hops_table(load_lines(lines))
        if with_route:
            return Computed(
                days,
                cols,
                route_rows(names, with_line=True),
                line_hours(True, days),
            )
        return Computed(days, cols, line_rows(names), line_hours(False, days))
    return Computed(
        days,
        cols,
        route_rows(names, with_line=False),
        route_hours(days),
        service=route_service(manifest, groups),
    )
