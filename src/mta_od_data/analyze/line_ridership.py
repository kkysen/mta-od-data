"""Riders on each line, and per route km and train-km,
from `mta-od-data raptor assign-range`'s path Parquets and their GTFS feeds.

A path counts towards a line if any of its rides is on one of the line's routes,
once however many of them it rides:
someone riding the 2 then the 3 is one 7 Av rider, but a 7 rider and an E rider.
That's riders, not passenger-km: a rider counts the same for one stop or the whole line.

A line's route km is the track its regular weekday service runs:
stop-to-stop segments at least `REGULAR_SHARE` of a route's weekday trips run,
so a few trips a day to a far terminal don't double a line's length.
Segments one of the line's trips skips past (express over local) don't add to it.
Train-km is every trip on the date, at its own length, rare ones included.
Lengths are along the feed's shapes.
"""

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from csv import DictReader
from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from functools import cache
from io import TextIOWrapper
from itertools import pairwise
from pathlib import Path
from statistics import median
from typing import Annotated
from zipfile import ZipFile

from typer import Option, Typer

from mta_od_data.analyze.common import Coord, connection, haversine
from mta_od_data.analyze.track_ridership import DEFAULT_MANIFEST
from mta_od_data.gtfs import DEFAULT_GTFS_DIR

app = Typer()

# The share of a route's weekday trips a segment needs to count towards its route km.
REGULAR_SHARE = 0.10

# Lines by trunk, as the MTA colors them, with their express variants.
TRUNKS: dict[str, frozenset[str]] = {
    "8 Av (A C E)": frozenset({"A", "C", "E"}),
    "6 Av (B D F M)": frozenset({"B", "D", "F", "FX", "M"}),
    "Broadway (N Q R W)": frozenset({"N", "Q", "R", "W"}),
    "Lexington Av (4 5 6)": frozenset({"4", "5", "6", "6X"}),
    "7 Av (1 2 3)": frozenset({"1", "2", "3"}),
    "Flushing (7)": frozenset({"7", "7X"}),
    "Canarsie (L)": frozenset({"L"}),
    "Nassau St (J Z)": frozenset({"J", "Z"}),
    "Crosstown (G)": frozenset({"G"}),
    "Shuttles (GS FS H)": frozenset({"GS", "FS", "H"}),
}

# Express variants the feed lists as routes of their own.
EXPRESS_VARIANTS = {"6X": "6", "7X": "7", "FX": "F"}

# Routes in the feed but not the OD data, which is subway only.
NOT_IN_OD = frozenset({"SI"})


class Grouping(StrEnum):
    ROUTE = "route"
    LINE = "line"
    TRUNK = "trunk"


def group_of(route: str, grouping: Grouping) -> str | None:
    if route in NOT_IN_OD:
        return None
    match grouping:
        case Grouping.ROUTE:
            return route
        case Grouping.LINE:
            return EXPRESS_VARIANTS.get(route, route)
        case Grouping.TRUNK:
            return next((t for t, rs in TRUNKS.items() if route in rs), None)


# Riders on paths with a ride on each group's routes, each path once per group.
# A ride is `<route> <stop>>...`; walks don't count.
RIDERS_QUERY = """
    WITH groups AS (
        SELECT DISTINCT path, map_from_entries($groups)[split_part(leg, ' ', 1)] AS grp
        FROM (
            SELECT path, unnest(string_split(path, ' | ')) AS leg
            FROM (SELECT DISTINCT path FROM read_parquet($paths))
        )
        WHERE NOT starts_with(leg, 'walk ')
    )
    SELECT grp, sum(riders)
    FROM read_parquet($paths) JOIN groups USING (path)
    WHERE grp IS NOT NULL
    GROUP BY grp
"""


def riders_by_group(paths: Path, groups: Mapping[str, str]) -> dict[str, float]:
    """Riders in one path Parquet on each group, from each route's group."""
    entries = [{"k": route, "v": group} for route, group in groups.items()]
    rows = (
        connection()
        .execute(RIDERS_QUERY, {"paths": str(paths), "groups": entries})
        .fetchall()
    )
    return {group: float(riders) for group, riders in rows}


type Segment = frozenset[str]


@dataclass(frozen=True, slots=True)
class Pattern:
    """Trips of one route stopping at the same parent stops along the same shape."""

    route: str
    service: str
    stops: tuple[str, ...]
    # Metres between each pair of consecutive stops.
    lengths: tuple[float, ...]

    @property
    def segments(self) -> Iterable[Segment]:
        return (frozenset(pair) for pair in pairwise(self.stops))


def along_shape(shape: list[Coord], stops: list[Coord]) -> list[float]:
    """Metres along `shape` between consecutive `stops`,
    each stop at the nearest shape point at or after the previous stop's.
    Straight lines if there's no shape."""
    if not shape:
        return [haversine(a, b) for a, b in pairwise(stops)]
    cumulative = [0.0]
    for a, b in pairwise(shape):
        cumulative.append(cumulative[-1] + haversine(a, b))
    indices: list[int] = []
    start = 0
    for stop in stops:
        distances = [haversine(point, stop) for point in shape[start:]]
        start += distances.index(min(distances))
        indices.append(start)
    return [cumulative[j] - cumulative[i] for i, j in pairwise(indices)]


@dataclass(frozen=True, slots=True)
class Feed:
    # Pattern and its trip count, across all services.
    patterns: dict[Pattern, int]
    # `calendar.txt` rows: service, weekdays it runs (Monday is 0), first and last date.
    calendar: list[tuple[str, frozenset[int], date, date]]
    # `calendar_dates.txt`: (service, date) to whether it's added (or removed).
    exceptions: dict[tuple[str, date], bool]

    def services_on(self, day: date) -> set[str]:
        services = {
            service
            for service, weekdays, first, last in self.calendar
            if day.weekday() in weekdays and first <= day <= last
        }
        for (service, d), added in self.exceptions.items():
            if d == day:
                if added:
                    services.add(service)
                else:
                    services.discard(service)
        return services

    def patterns_on(self, day: date) -> dict[Pattern, int]:
        services = self.services_on(day)
        return {p: n for p, n in self.patterns.items() if p.service in services}


def parse_date(s: str) -> date:
    return date(int(s[:4]), int(s[4:6]), int(s[6:]))


@cache
def load_feed(path: Path) -> Feed:
    with ZipFile(path) as z:

        def rows(name: str) -> Iterable[dict[str, str]]:
            with z.open(name) as f:
                yield from DictReader(TextIOWrapper(f, encoding="utf-8-sig"))

        coords = {
            r["stop_id"]: Coord(float(r["stop_lat"]), float(r["stop_lon"]))
            for r in rows("stops.txt")
        }
        points: defaultdict[str, list[tuple[int, Coord]]] = defaultdict(list)
        for r in rows("shapes.txt"):
            coord = Coord(float(r["shape_pt_lat"]), float(r["shape_pt_lon"]))
            points[r["shape_id"]].append((int(r["shape_pt_sequence"]), coord))
        shapes = {s: [c for _, c in sorted(ps)] for s, ps in points.items()}
        trips = {
            r["trip_id"]: (r["route_id"], r["service_id"], r["shape_id"])
            for r in rows("trips.txt")
        }
        stop_times: defaultdict[str, list[tuple[int, str]]] = defaultdict(list)
        for r in rows("stop_times.txt"):
            stop_times[r["trip_id"]].append((int(r["stop_sequence"]), r["stop_id"]))
        calendar = [
            (
                r["service_id"],
                frozenset(
                    i
                    for i, d in enumerate(
                        (
                            "monday",
                            "tuesday",
                            "wednesday",
                            "thursday",
                            "friday",
                            "saturday",
                            "sunday",
                        )
                    )
                    if r[d] == "1"
                ),
                parse_date(r["start_date"]),
                parse_date(r["end_date"]),
            )
            for r in rows("calendar.txt")
        ]
        exceptions = {
            (r["service_id"], parse_date(r["date"])): r["exception_type"] == "1"
            for r in rows("calendar_dates.txt")
        }

    keys: Counter[tuple[str, str, str, tuple[str, ...]]] = Counter()
    for trip, times in stop_times.items():
        route, service, shape = trips[trip]
        keys[route, service, shape, tuple(s for _, s in sorted(times))] += 1
    patterns: Counter[Pattern] = Counter()
    for (route, service, shape, stops), n in keys.items():
        lengths = along_shape(shapes.get(shape, []), [coords[s] for s in stops])
        # Parent stops: `101N` is `101`'s northbound platform.
        parents = tuple(s[:-1] for s in stops)
        patterns[Pattern(route, service, parents, tuple(lengths))] += n
    return Feed(dict(patterns), calendar, exceptions)


def segment_lengths(patterns: Iterable[Pattern]) -> dict[Segment, float]:
    """Each segment's median measured length, across patterns and directions."""
    measured: defaultdict[Segment, list[float]] = defaultdict(list)
    for p in patterns:
        for segment, length in zip(p.segments, p.lengths, strict=True):
            measured[segment].append(length)
    return {s: median(ls) for s, ls in measured.items()}


def regular_segments(patterns: Mapping[Pattern, int]) -> set[Segment]:
    """Segments at least `REGULAR_SHARE` of these trips run."""
    trips: Counter[Segment] = Counter()
    for p, n in patterns.items():
        for segment in set(p.segments):
            trips[segment] += n
    total = sum(patterns.values())
    return {s for s, n in trips.items() if n >= REGULAR_SHARE * total}


def route_length(
    patterns: Mapping[Pattern, int], lengths: Mapping[Segment, float]
) -> float:
    """Metres of track the routes of `patterns` regularly run, each segment once."""
    by_route: defaultdict[str, dict[Pattern, int]] = defaultdict(dict)
    for p, n in patterns.items():
        by_route[p.route][p] = n
    segments = set[Segment]().union(*(regular_segments(ps) for ps in by_route.values()))
    positions = [{s: i for i, s in enumerate(p.stops)} for p in patterns]

    def skipped(segment: Segment) -> bool:
        if len(segment) < 2:
            return False
        a, b = segment
        return any(a in q and b in q and abs(q[a] - q[b]) > 1 for q in positions)

    return sum(lengths[s] for s in segments if not skipped(s))


@dataclass(slots=True)
class Totals:
    riders: float = 0.0
    route_km: float = 0.0
    trips: float = 0.0
    train_km: float = 0.0

    def add(self, other: Totals, days: int) -> None:
        self.riders += other.riders * days
        self.route_km += other.route_km * days
        self.trips += other.trips * days
        self.train_km += other.train_km * days

    def per_day(self, days: int) -> Totals:
        return Totals(
            self.riders / days,
            self.route_km / days,
            self.trips / days,
            self.train_km / days,
        )


def day_totals(
    paths: Path, feed: Feed, day: date, grouping: Grouping
) -> dict[str, Totals]:
    patterns = feed.patterns_on(day)
    lengths = segment_lengths(patterns)
    groups = {
        p.route: g for p in patterns if (g := group_of(p.route, grouping)) is not None
    }
    by_group: defaultdict[str, dict[Pattern, int]] = defaultdict(dict)
    for p, n in patterns.items():
        if p.route in groups:
            by_group[groups[p.route]][p] = n
    riders = riders_by_group(paths, groups)
    return {
        group: Totals(
            riders=riders.get(group, 0.0),
            route_km=route_length(ps, lengths) / 1000,
            trips=sum(ps.values()),
            train_km=sum(n * sum(p.lengths) for p, n in ps.items()) / 1000,
        )
        for group, ps in by_group.items()
    }


@app.command()
def line_ridership(
    by: Annotated[
        Grouping,
        Option(
            help=(
                "route: each GTFS route, express variants (6X 7X FX) apart; "
                "line: express variants with their line; trunk: lines by trunk color"
            )
        ),
    ] = Grouping.LINE,
    manifest: Annotated[
        Path, Option(help="`mta-od-data raptor assign-range`'s manifest")
    ] = DEFAULT_MANIFEST,
) -> None:
    """Average weekday riders on each line, per route km, and per train-km,
    over `mta-od-data raptor assign-range`'s dates.

    Each date stands for its `days`, so the averages weight it by them,
    route km and train-km included, from each date's own feed.
    """
    totals: defaultdict[str, Totals] = defaultdict(Totals)
    total_days = 0
    with manifest.open() as f:
        for row in DictReader(f):
            # Found beside the manifest, as in `track-ridership`.
            paths = manifest.parent / Path(row["paths"]).name
            feed = load_feed(DEFAULT_GTFS_DIR / Path(row["feed"]).name)
            days = int(row["days"])
            day = date.fromisoformat(row["date"])
            for group, t in day_totals(paths, feed, day, grouping=by).items():
                totals[group].add(t, days)
            total_days += days

    averages = {g: t.per_day(total_days) for g, t in totals.items()}
    print(f"Average weekday over {total_days} weekdays.")
    print()
    print(
        f"| {by} | riders | route km | riders per route km "
        "| trips | train-km | riders per train-km |"
    )
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")

    def riders(group: str) -> float:
        return averages[group].riders

    for group in sorted(averages, key=riders, reverse=True):
        t = averages[group]
        print(
            f"| {group} | {t.riders:,.0f} | {t.route_km:.1f} "
            f"| {t.riders / t.route_km:,.0f} | {t.trips:,.0f} "
            f"| {t.train_km:,.0f} | {t.riders / t.train_km:.1f} |"
        )
