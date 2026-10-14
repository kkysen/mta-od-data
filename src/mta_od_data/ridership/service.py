"""Each route's track and trips on a date, from its GTFS feed:
route km, trips, and train-km for `mta-od-data ridership --by route`,
and each route's platforms' directions.

A route's route km is the track its regular weekday service runs:
stop-to-stop segments at least `REGULAR_SHARE` of a route's weekday trips run,
so a few trips a day to a far terminal don't double a line's length.
Segments one of its trips skips past (express over local) don't add to it.
Train-km is every trip on the date, at its own length, rare ones included.
Lengths are along the feed's shapes.
"""

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from csv import DictReader
from dataclasses import dataclass
from datetime import date
from functools import cache
from io import TextIOWrapper
from itertools import pairwise
from pathlib import Path
from statistics import median
from zipfile import ZipFile

from mta_od_data.analyze.common import Coord, haversine

# The share of a route's weekday trips a segment needs to count towards its route km.
REGULAR_SHARE = 0.10

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
    # Each route's consecutive parent stops to their platforms' directions,
    # e.g. ("1", "120", "121"): ("N", "N") for `120N` then `121N`.
    directions: dict[tuple[str, str, str], tuple[str, str]]

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
    directions: dict[tuple[str, str, str], tuple[str, str]] = {}
    for (route, service, shape, stops), n in keys.items():
        for a, b in pairwise(stops):
            directions[route, a[:-1], b[:-1]] = (a[-1], b[-1])
        lengths = along_shape(shapes.get(shape, []), [coords[s] for s in stops])
        # Parent stops: `101N` is `101`'s northbound platform.
        parents = tuple(s[:-1] for s in stops)
        patterns[Pattern(route, service, parents, tuple(lengths))] += n
    return Feed(dict(patterns), calendar, exceptions, directions)


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
