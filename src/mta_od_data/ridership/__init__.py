"""Average weekday ridership by station complex, station, station direction, route,
or line,
from `mta-od-data raptor assign-range`'s paths.

Each measure is a sum of paths' riders, so it's taken over
`average_path_riders`' average of each path over the manifest's dates,
once per way of counting riders (a column each):
as in the OD data, and scaled by each `--od-factors` file,
all with fare evaders unless `--no-fare-evasion`.

- A place (complex, station, station direction)
  counts each ride's boarding and alighting there,
  which of those are transfers (not the journey's first boarding or last alighting),
  and riders staying on a train stopping there.
  With `--route` but not `--by route`, consecutive rides on `--route`'s routes
  changing at the same stop are one ride: an N to R change at 59 St is neither.
- A route counts each journey riding it once, however many of its rides are on it.
  Routes with express variants (5X 6X 7X FX) count as the route, `5`,
  and again as their local, `5L`, or express, `5X`, alone.
- A line counts each journey with a ride on its track once:
  between two consecutive stops both on it (`lines.json5`), as `raptor` paths
  list every stop a ride passes.
"""

from collections import defaultdict
from collections.abc import Iterable, Sequence
from csv import DictReader
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Annotated, Any

import json5
from typer import BadParameter, Context, Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import (
    Complex,
    MissingComplex,
    abbreviate_name,
    connection,
    display_station,
)
from mta_od_data.analyze.markdown import table_row, table_rule
from mta_od_data.analyze.path_riders import (
    AveragePaths,
    average_path_riders,
    counting,
    load_fare_evasion,
    read_manifest,
)
from mta_od_data.gtfs import DEFAULT_GTFS_DIR
from mta_od_data.invocation import produced_by
from mta_od_data.ridership.service import (
    Pattern,
    load_feed,
    route_length,
    segment_lengths,
)
from mta_od_data.ridership.trips import (
    Train,
    crowded_trains,
    line_hours,
    load_trip_stops,
    place_hours,
    route_hours,
)

app = Typer()

HERE = Path(__file__).parent
DEFAULT_MANIFEST = DATA / "raptor" / "manifest.csv"
# Scaled to 2019's counted entries (`scale-od --to-counts`), before the pandemic.
# Not also to the OD data's own year's: its trips are within ~1% of 2025's counts
# systemwide, and 2% at 80% of stations, so that column barely differed.
DEFAULT_OD_FACTORS = [DATA / "mta_od_2019_counted.factors.parquet"]
DEFAULT_LINES = HERE / "lines.json5"
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


DEFAULT_STATIONS = DATA / "stations.csv"
DEFAULT_COMPLEXES = DATA / "complexes.csv"


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


@dataclass(frozen=True, slots=True)
class Names:
    """Stations' and complexes' names, and stations' complexes and directions."""

    station: dict[str, str]
    complex_of: dict[str, str]
    complex: dict[str, str]
    direction: dict[tuple[str, str], str] = field(default_factory=dict)
    # Each station's name alone, without its routes.
    stop: dict[str, str] = field(default_factory=dict)


def load_names(stations: Path, complexes: Path) -> Names:
    """Names as the `analyze` reports write them: `abbreviate_name`d,
    with their routes as `display_station` lists them, `DeKalb Av (B,Q,R)`."""
    with stations.open() as f:
        rows = list(DictReader(f))
    complex_names = {
        str(c.complex_id): c.display()
        for c in Complex.load_all(complexes)
        if not isinstance(c, MissingComplex)
    }
    return Names(
        station={
            r["gtfs_stop_id"]: display_station(
                abbreviate_name(r["stop_name"]), frozenset(r["daytime_routes"].split())
            )
            for r in rows
        },
        complex_of={r["gtfs_stop_id"]: r["complex_id"] for r in rows},
        stop={r["gtfs_stop_id"]: abbreviate_name(r["stop_name"]) for r in rows},
        complex=complex_names,
        direction={
            (r["gtfs_stop_id"], d): r[f"{label}_direction_label"]
            for r in rows
            for d, label in [("N", "north"), ("S", "south")]
        },
    )


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
    and train-km times its trains' lengths in 60-ft cars' worth."""

    route_km: float = 0.0
    trips: float = 0.0
    train_km: float = 0.0
    train_60ft_km: float = 0.0


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
            t.train_60ft_km += (
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
            t.train_60ft_km / total_days,
        )
        for g, t in totals.items()
    }


def route_rows(names: list[str], with_line: bool) -> list[tuple[Any, ...]]:
    line = ", name" if with_line else ""
    on_line = "JOIN on_line USING (path, route, i)" if with_line else ""
    sums = ", ".join(f"sum({n})::DOUBLE" for n in names)
    return (
        connection()
        .execute(
            f"""
            WITH {ON_LINE if with_line else "x AS (SELECT 1)"},
            journeys AS (
                SELECT DISTINCT path, grp{line}, {", ".join(names)}
                FROM legs JOIN route_groups USING (route) {on_line}
            )
            SELECT grp{line}, {sums} FROM journeys GROUP BY ALL
            """,
            {"lines": lines_param()} if with_line else {},
        )
        .fetchall()
    )


# Each ride on each line's track, by the leg it's in.
ON_LINE = """
    on_line AS (
        SELECT path, route, i, l.name
        FROM legs, (SELECT unnest($lines) AS l)
        WHERE route IN (SELECT route FROM route_groups)
        AND len(list_filter(
            range(1, len(stops)),
            j -> list_contains(l.stops, stops[j])
                AND list_contains(l.stops, stops[j + 1])
        )) > 0
    )
"""

LINES: dict[str, list[str]] = {}


def lines_param() -> list[dict[str, object]]:
    return [{"name": n, "stops": s} for n, s in LINES.items()]


def load_lines(path: Path) -> dict[str, list[str]]:
    lines = json5.loads(path.read_text(), allow_duplicate_keys=False)
    return {name: list(line["stops"]) for name, line in lines.items()}


def line_rows(names: list[str]) -> list[tuple[Any, ...]]:
    sums = ", ".join(f"sum({n})::DOUBLE" for n in names)
    return (
        connection()
        .execute(
            f"""
            WITH {ON_LINE},
            journeys AS (
                SELECT DISTINCT path, name, {", ".join(names)}
                FROM legs JOIN on_line USING (path, route, i)
            )
            SELECT name, {sums} FROM journeys GROUP BY ALL
            """,
            {"lines": lines_param()},
        )
        .fetchall()
    )


def busiest(
    rows: Iterable[tuple[Any, ...]],
) -> dict[tuple[Any, ...], tuple[int, float]]:
    """Each key's busiest hour and its riders, from `(*key, hour, riders)` rows:
    the earliest of any tied."""
    by_key: defaultdict[tuple[Any, ...], dict[int, float]] = defaultdict(dict)
    for *key, hour, riders in sorted(rows, key=as_text):
        hours = by_key[tuple(key)]
        hours[hour] = hours.get(hour, 0.0) + riders

    def most(hour_riders: tuple[int, float]) -> tuple[int, int]:
        hour, riders = hour_riders
        return (round(riders), -hour)

    return {k: max(hours.items(), key=most) for k, hours in by_key.items()}


def peak_heads(cols: Sequence[Column]) -> list[str]:
    return ["Busiest Hour", f"Riders in It, {cols[0].label}"]


def peak_cells(
    peaks: dict[tuple[Any, ...], tuple[int, float]], key: tuple[Any, ...]
) -> list[str]:
    if key not in peaks:
        return ["", ""]
    hour, riders = peaks[key]
    return [clock(hour), fmt(riders)]


def clock(hour: int) -> str:
    """A service day's hour, from 4 to 27, as the hour of the day it starts."""
    return f"{hour % 24:02}:00"


def as_text(row: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(map(str, row))


def by_riders(row: tuple[Any, ...]) -> tuple[int, str]:
    """A `(name, riders, ...)` row's order: busiest first, as shown."""
    return (-round(row[1]), row[0])


def by_line_then_riders(row: tuple[Any, ...]) -> tuple[str, int, str]:
    """A `(route, line, riders, ...)` row's order."""
    return (row[1], -round(row[2]), row[0])


def fmt(x: float | None, digits: int = 0) -> str:
    return f"{x or 0:,.{digits}f}"


def platform_labels(names: Names) -> dict[str, str]:
    """Each platform's station and what it serves, from `directions`:
    e.g. `96 St (1,2,3), Uptown 1 2 3`, or both directions for an island."""
    rows = (
        connection()
        .execute(
            """
            SELECT platform, stop, dir, list(DISTINCT route ORDER BY route)
            FROM (
                SELECT pa AS platform, a AS stop, da AS dir, route FROM directions
                UNION ALL
                SELECT pb, b, db, route FROM directions
            )
            WHERE platform != ''
            GROUP BY ALL
            ORDER BY ALL
            """
        )
        .fetchall()
    )
    served: defaultdict[str, list[str]] = defaultdict(list)
    station: dict[str, str] = {}
    for platform, stop, d, routes in rows:
        station.setdefault(platform, names.station.get(stop, stop))
        where = names.direction.get((stop, d), d)
        served[platform].append(f"{where} {' '.join(routes)}")
    return {p: f"{station[p]}, {' & '.join(s)}" for p, s in served.items()}


def place_table(
    by: By,
    with_route: bool,
    rows: list[tuple[Any, ...]],
    hours: list[tuple[Any, ...]],
    cols: list[Column],
    names_: Names,
) -> list[str]:
    """`place_rows`' rows as a table, with each place's busiest hour
    from `hours`, `(stop, dir, platform, [route,] hour, riders on + off)` rows."""
    platform_names = platform_labels(names_) if by is By.PLATFORM else {}

    def label(stop: str, d: str, platform: str) -> tuple[str, ...]:
        match by:
            case By.COMPLEX:
                c = names_.complex_of.get(stop, "")
                return (names_.complex.get(c, c),)
            case By.STATION:
                return (names_.station.get(stop, stop),)
            case By.STATION_DIRECTION:
                where = names_.direction.get((stop, d), d)
                return names_.station.get(stop, stop), where
            case By.PLATFORM:
                if platform:
                    return (platform_names.get(platform, platform),)
                # A stop OSM's routes don't say the platform of: its direction.
                where = names_.direction.get((stop, d), d)
                name = names_.station.get(stop, stop)
                return (f"{name}, {where}, platform unknown",)
        raise AssertionError(by)

    # Complexes sum their stations' rows.
    k = len(cols)
    merged: defaultdict[tuple[str, ...], list[float]] = defaultdict(
        lambda: [0.0] * (k + 4)
    )

    def identity(stop: str, d: str, platform: str) -> tuple[str, ...]:
        """The place a row is at, which its name must be unique to."""
        match by:
            case By.COMPLEX:
                return (names_.complex_of.get(stop, ""),)
            case By.STATION:
                return (stop,)
            case By.STATION_DIRECTION:
                return (stop, d)
            case By.PLATFORM:
                return (platform,) if platform else (stop, d)
        raise AssertionError(by)

    named: dict[tuple[str, ...], tuple[str, ...]] = {}
    # In a set order, so a complex's floating-point sum of its stations is too.
    for row in sorted(rows, key=as_text):
        stop, d, platform, *rest = row
        grp = (rest.pop(0),) if with_route else ()
        key = (*label(stop, d, platform), *grp)
        place = identity(stop, d, platform)
        if named.setdefault(key, place) != place:
            raise ValueError(f"{named[key]} and {place} are both named {key}")
        for j, v in enumerate(rest):
            merged[key][j] += v or 0.0
    peaks = busiest((*label(stop, d, p), *rest) for stop, d, p, *rest in hours)
    head = [
        *(
            ["Station", "Direction"]
            if by is By.STATION_DIRECTION
            else [by.value.title()]
        ),
        *(["Route"] if with_route else []),
    ]
    lines = [
        table_row(
            *head,
            *(f"On + Off, {c.label}" for c in cols),
            f"On, {cols[0].label}",
            f"Off, {cols[0].label}",
            f"Transfers On + Off, {cols[0].label}",
            f"Staying On, {cols[0].label}",
            "Busiest Hour",
            f"On + Off in It, {cols[0].label}",
        ),
        table_rule("l" * len(head) + "r" * (k + 4) + "lr"),
    ]

    # By the riders as shown, so rows that show the same come out in a set order.
    def by_riders_shown(
        item: tuple[tuple[str, ...], list[float]],
    ) -> tuple[int, tuple[str, ...]]:
        key, vs = item
        return (-round(vs[0]), key)

    for key, vs in sorted(merged.items(), key=by_riders_shown):
        hour, riders = peaks.get(key, (None, 0.0))
        peak = (clock(hour), fmt(riders)) if hour is not None else ("", "")
        lines.append(table_row(*key, *(fmt(v) for v in vs), *peak))
    return lines


def route_order(riders: dict[str, float]) -> list[str]:
    """Busiest first, each route's variants right after it."""

    def order(g: str) -> tuple[int, str, bool, str]:
        base = base_route(g)
        return (-round(riders.get(base, 0.0)), base, g != base, g)

    return sorted(riders, key=order)


@app.command()
def ridership(
    ctx: Context,
    by: Annotated[
        list[By],
        Option(
            help=(
                "What to total riders by; repeat to cross one of "
                "complex, station, station-direction, or line with route"
            )
        ),
    ],
    route: Annotated[
        list[str] | None,
        Option(
            help=(
                "Only rides on these `--by route` rows (repeatable), "
                "e.g. --route 1, or --route N --route R --route W as one group"
            )
        ),
    ] = None,
    manifest: Annotated[
        Path, Option(help="`mta-od-data raptor assign-range`'s manifest")
    ] = DEFAULT_MANIFEST,
    od_factors: Annotated[
        list[Path] | None,
        Option(
            help=(
                "Count riders as if routed with OD data scaled by these factors "
                "(repeatable, a column each), from `mta-od-data scale-od`; "
                "by default 2019's counted entries"
            )
        ),
    ] = None,
    unscaled: Annotated[
        bool, Option(help="Count riders as in the OD data, unscaled, first")
    ] = True,
    fare_evasion: Annotated[
        bool,
        Option(
            help=(
                "Count fare evaders too: riders over 1 less the evasion rate "
                "in each date's quarter, or in the year scaled to"
            )
        ),
    ] = True,
    lines: Annotated[Path, Option(help="Named lines for --by line")] = DEFAULT_LINES,
    top: Annotated[
        int, Option(help="--by trip: each route's this many most crowded trains")
    ] = 1,
    markdown_out: Annotated[
        Path | None, Option(help="Write the report here, not to stdout")
    ] = None,
) -> None:
    """Average weekday ridership by station complex, station, station direction,
    route, or line,
    over `mta-od-data raptor assign-range`'s dates.
    """
    route = route or []
    if od_factors is None:
        od_factors = DEFAULT_OD_FACTORS
    dims = set(by)
    evasion = load_fare_evasion(None) if fare_evasion else None
    if By.TRIP in dims:
        if len(dims) > 1:
            raise BadParameter("trip goes alone", param_hint="--by")
        days = load_trip_stops(manifest, evasion).days
        table = trip_table(
            crowded_trains(trip_routes(route), top),
            load_names(DEFAULT_STATIONS, DEFAULT_COMPLEXES),
            period(manifest),
        )
        report = render(ctx, by, route, manifest, days, [], fare_evasion, table)
        write(report, markdown_out)
        return
    places = dims & PLACES
    if (
        len(dims) != len(by)
        or len(places) > 1
        or (places and By.LINE in dims)
        or (len(dims) > 1 and By.ROUTE not in dims)
    ):
        raise BadParameter(
            "one of complex, station, station-direction, route, or line, "
            "optionally crossed with route",
            param_hint="--by",
        )
    cols = columns(manifest, od_factors, fare_evasion, unscaled)
    names = load_legs(cols)
    kept, groups = ride_routes(route)
    route_groups_table(groups)
    with_route = By.ROUTE in dims and len(dims) > 1
    days = load_trip_stops(manifest, evasion).days

    if places:
        (place,) = places
        directions_table(manifest)
        build_events(kept, names, merge=bool(route) and not with_route)
        rows = place_rows(with_route, names)
        table = place_table(
            place,
            with_route,
            rows,
            place_hours(with_route, days),
            cols,
            load_names(DEFAULT_STATIONS, DEFAULT_COMPLEXES),
        )
    elif By.LINE in dims:
        LINES.clear()
        LINES.update(load_lines(lines))
        if with_route:
            got = route_rows(names, with_line=True)
            peaks = busiest(line_hours(lines_param(), True, days))
            table = [
                table_row("Line", "Route", *(c.label for c in cols), *peak_heads(cols)),
                table_rule("ll" + "r" * len(cols) + "lr"),
            ]
            for g, name, *vs in sorted(got, key=by_line_then_riders):
                if not route or g in route:
                    table.append(
                        table_row(
                            name,
                            g,
                            *(fmt(v) for v in vs),
                            *peak_cells(peaks, (name, g)),
                        )
                    )
        else:
            got = line_rows(names)
            peaks = busiest(line_hours(lines_param(), False, days))
            table = [
                table_row("Line", *(c.label for c in cols), *peak_heads(cols)),
                table_rule("l" + "r" * len(cols) + "lr"),
            ]
            for name, *vs in sorted(got, key=by_riders):
                table.append(
                    table_row(name, *(fmt(v) for v in vs), *peak_cells(peaks, (name,)))
                )
    else:
        got = {grp: vs for grp, *vs in route_rows(names, with_line=False)}
        if route:
            got = {g: vs for g, vs in got.items() if g in route}
        service = route_service(manifest, groups)
        peaks = busiest(route_hours(days))
        first = cols[0].label
        table = [
            table_row(
                "Route",
                *(c.label for c in cols),
                "Route-km",
                f"Per Route-km, {first}",
                "Trips",
                "Train-km",
                f"Per Train-km, {first}",
                f"Per {CAR_FT} ft of Train-km, {first}",
                *peak_heads(cols),
            ),
            table_rule("l" + "r" * (len(cols) + 6) + "lr"),
        ]
        for grp in route_order({g: vs[0] for g, vs in got.items()}):
            s = service.get(grp, RouteService())
            vs = got[grp]
            table.append(
                table_row(
                    grp,
                    *(fmt(v) for v in vs),
                    fmt(s.route_km, 1),
                    fmt(vs[0] / s.route_km if s.route_km else None),
                    fmt(s.trips),
                    fmt(s.train_km),
                    fmt(vs[0] / s.train_km if s.train_km else None, 1),
                    fmt(vs[0] / s.train_60ft_km if s.train_60ft_km else None, 2),
                    *peak_cells(peaks, (grp,)),
                )
            )

    report = render(ctx, by, route, manifest, days, cols, fare_evasion, table)
    write(report, markdown_out)


def write(report: str, markdown_out: Path | None) -> None:
    if markdown_out is None:
        print(report, end="")
    else:
        markdown_out.write_text(report)
        print(f"Wrote {markdown_out}")


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


def clock_time(secs: int) -> str:
    """Seconds on the service day's clock as a time of day, `HH:MM`."""
    return f"{secs // 3600 % 24:02}:{secs % 3600 // 60:02}"


def trip_table(trains: list[Train], names: Names, label: str) -> list[str]:
    def stop(s: str) -> str:
        return names.stop.get(s, s)

    lengths = load_train_lengths()

    lines = [
        table_row(
            "Route",
            "Train",
            f"Peak Load, {label}",
            "Train Length (ft)",
            f"Peak per {CAR_FT} ft",
            "Peak Between",
            "Leaving At",
            "Weekdays Run",
        ),
        table_rule("llrrrllr"),
    ]
    for t in trains:
        lines.append(
            table_row(
                t.route,
                f"{clock_time(t.first_departure)} {stop(t.first_stop)}"
                f" to {stop(t.last_stop)}",
                fmt(t.peak),
                fmt(lengths.get(t.route)),
                fmt(t.peak / lengths[t.route] * CAR_FT if t.route in lengths else None),
                f"{stop(t.peak_stop)} to {stop(t.peak_next)}",
                clock_time(t.peak_departure),
                str(t.days),
            )
        )
    return lines


def render(
    ctx: Context,
    by: Iterable[By],
    route: Sequence[str],
    manifest: Path,
    days: int,
    cols: Sequence[Column],
    fare_evasion: bool,
    table: list[str],
) -> str:
    dates = sorted(row["date"] for row in read_manifest(manifest))
    scope = f" on {', '.join(route)}" if route else ""
    evaders = " with fare evaders" if fare_evasion else ""
    lines = [
        f"# Ridership by {' and '.join(b.value.replace('-', ' ') for b in by)}{scope}",
        "",
        f"Average weekday riders{evaders}, "
        f"over {days} weekdays from {dates[0]} to {dates[-1]} "
        f"(`{manifest}`).",
        *(
            f"The {c.label} column scales the OD data on these dates "
            f"to {c.scaled_to}'s counted station entries."
            for c in cols
            if c.scaled_to is not None
        ),
        *(
            [
                "The busiest hour is the hour, by when it starts, "
                f"with the most riders in the {cols[0].label} column "
                "on its trains there "
                "(getting on or off at a place, boarding a route, or joining a line), "
                "and those riders."
            ]
            if cols
            else [
                "A train's load is its riders on board between two stops, "
                "averaged over the weekdays it runs: "
                "a train is the same on any date with the same route, direction, "
                "first stop, and departure from it."
            ]
        ),
        *(
            [
                "Platforms are from OpenStreetMap's subway routes "
                "(© OpenStreetMap contributors, ODbL), "
                "by `mta-od-data fetch-platforms`."
            ]
            if By.PLATFORM in by
            else []
        ),
        "",
        f"Produced by `{produced_by(ctx)}`.",
        "",
        *table,
    ]
    return "\n".join(lines) + "\n"
