import csv
from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from functools import cache
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from typing import Protocol, Self

import duckdb


class DayType(StrEnum):
    WEEKDAY = "weekday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    ALL = "all"


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
DAY_TYPE_PRESETS: dict[DayType, tuple[str, ...] | None] = {
    DayType.WEEKDAY: WEEKDAYS,
    DayType.SATURDAY: ("Saturday",),
    DayType.SUNDAY: ("Sunday",),
    DayType.ALL: None,
}


def abbreviate_name(name: str) -> str:
    """Shorter forms for station names that are unwieldy at full length,
    especially with a route list appended.
    A plain substring replacement,
    so it also shortens merged complex names containing the long form
    (e.g. "Chambers St/WTC/Park Place/Cortlandt St")."""
    abbreviations = (
        ("Atlantic Av-Barclays Ctr", "Atlantic Av"),
        ("Port Authority Bus Terminal", "PABT"),
        ("Park Place", "Park Pl"),
    )
    for long, short in abbreviations:
        name = name.replace(long, short)
    return name


@dataclass(slots=True, frozen=True)
class Coord:
    lat: float
    lon: float


class Place(Protocol):
    """Somewhere a `regions.Region` can be asked about.

    A `Complex` and a `Station` are both one, and share nothing else:
    a region is about where a station is and which borough it's in,
    which is the one question that doesn't care whether it's being
    asked about a whole complex or one line's stop within it.
    """

    @property
    def loc(self) -> Coord: ...
    @property
    def borough(self) -> str: ...
    @property
    def cbd(self) -> bool: ...


@cache
def display_station(name: str, routes: frozenset[str]) -> str:
    """A station's name with the routes serving it, `"DeKalb Av (B,Q,R)"`.

    Shared by `Complex` and `Station` rather than inherited:
    the two agree on how a station reads, and on nothing else,
    since a complex's name and routes are the merge of its stations'
    (`"62 St/New Utrecht Av (D,N,W)"` over `"62 St (N,W)"`).
    """
    return f"{name} ({','.join(sorted(routes))})"


@dataclass(slots=True, frozen=True)
class Complex:
    """A station complex: everything a rider can reach without a
    MetroCard, which is what the OD data counts trips between.

    Its `name`, `routes`, and `loc` are the merge of the `Station`s in
    it, and differ from every one of them where the complex has more
    than one: the name lists them all, the routes are the union, and
    the point is a centroid that can sit well off any of the stations.
    """

    complex_id: int
    name: str
    routes: frozenset[str]
    # The complex's centroid, which is not any station's own point;
    # see `Station.loc` for when that difference matters.
    loc: Coord
    # "M"/"Bk"/"Bx"/"Q"/"SI", as given by the source data.
    borough: str
    # In Manhattan's Congestion Relief Zone; see `regions.cbd_region`.
    cbd: bool

    def display(self, routes: frozenset[str] | None = None) -> str:
        return display_station(self.name, self.routes if routes is None else routes)

    @classmethod
    def load(cls, row: dict[str, str]) -> Self:
        return cls(
            complex_id=int(row["complex_id"]),
            name=abbreviate_name(row["stop_name"]),
            routes=frozenset(row["daytime_routes"].split()),
            loc=Coord(lat=float(row["latitude"]), lon=float(row["longitude"])),
            borough=row["borough"],
            cbd=row["cbd"] == "true",
        )

    @classmethod
    def load_all(cls, path: Path) -> dict[int, Self]:
        """By id, which is also what interns them:
        one object per complex for the process's lifetime,
        so a `Station` can hold its own rather than an id to look up.
        """
        with path.open(newline="") as f:
            return {
                (complex_station := cls.load(row)).complex_id: complex_station
                for row in csv.DictReader(f)
            }


@dataclass(slots=True, frozen=True)
class Station:
    """One line's stop, which is what the reference data calls a
    station: `62 St` on the Sea Beach line, as against the
    `62 St/New Utrecht Av` complex it belongs to.

    Not a station, though the code used to call it one: the source has
    a row per (complex, line), both directions together, and express
    and local tracks together (`59 St-Columbus Circle` on `8th Av -
    Fulton St` is one row reading `A C B D`).
    """

    # The complex this is part of, rather than its id: `Complex.load_all`
    # interns them, so this is the one object for that complex, and the
    # code that used to look one up by id has it in hand.
    complex: Complex
    # This stop's own name and routes, which are the complex's only
    # where the complex is a single station: 86 of the 496 stations
    # serve routes their complex has more of, and 38 are named
    # differently.
    name: str
    routes: frozenset[str]
    # This stop's own point, not the complex's centroid, which for a
    # merged complex (e.g. Times Sq-42 St/PABT) can sit well away from
    # any of its stations and throw off a nearest-station distance.
    loc: Coord
    # Physical line name, e.g. "4th Av".
    line: str
    # The source data's own per-station id, which runs along the line,
    # so sorting by it puts a line's stations in the order they're
    # passed.
    # Not `gtfs_stop_id`, which also identifies a station but doesn't
    # sort the same way (its prefixes are per-service, so the Brighton
    # line's stations interleave `D` and `R` ids).
    station_id: int

    @property
    def complex_id(self) -> int:
        return self.complex.complex_id

    # Where a station is, is where its complex is: the two agree on
    # `borough` and `cbd` for all 496 of them, being the same place.
    @property
    def borough(self) -> str:
        return self.complex.borough

    @property
    def cbd(self) -> bool:
        return self.complex.cbd

    def display(self, routes: frozenset[str] | None = None) -> str:
        return display_station(self.name, self.routes if routes is None else routes)

    @classmethod
    def load(cls, row: dict[str, str], complexes: dict[int, Complex]) -> Self:
        return cls(
            complex=complexes[int(row["complex_id"])],
            name=abbreviate_name(row["stop_name"]),
            routes=frozenset(row["daytime_routes"].split()),
            loc=Coord(
                lat=float(row["gtfs_latitude"]), lon=float(row["gtfs_longitude"])
            ),
            line=row["line"],
            station_id=int(row["station_id"]),
        )

    @classmethod
    def load_all(cls, path: Path, complexes: dict[int, Complex]) -> list[Self]:
        with path.open(newline="") as f:
            return [cls.load(row, complexes) for row in csv.DictReader(f)]


@cache
def station_name(
    stations: tuple[Station, ...], complex_name: str, routes: frozenset[str]
) -> str:
    """`complex_name` narrowed to the stations `routes` actually stops at.

    A complex's name lists every station merged into it
    ("Chambers St/WTC/Park Pl/Cortlandt St"),
    which is the widest column in most reports
    and mostly about routes the row has nothing to do with.
    The R stops only at Cortlandt St there, so an `(R)` row says that.

    Only when the routes land on exactly one *named* station.
    Two names means the complex really is the smallest thing
    that covers them
    (Times Sq-42 St and 42 St-Port Authority Bus Terminal, for A,C,N),
    and several stations sharing one name collapse to it anyway
    (34 St-Herald Sq's 6 Av and Broadway stations).
    """
    names = {p.name for p in stations if p.routes & routes}
    return names.pop() if len(names) == 1 else complex_name


@dataclass(slots=True, frozen=True)
class ComplexStations:
    """The `Station`s in each complex, for `display`."""

    by_complex: dict[int, tuple[Station, ...]]

    @classmethod
    def build(cls, individual_stations: list[Station]) -> Self:
        by_complex: defaultdict[int, list[Station]] = defaultdict(list)
        for station in individual_stations:
            by_complex[station.complex_id].append(station)
        return cls(
            by_complex={cid: tuple(v) for cid, v in by_complex.items()},
        )

    def name(self, complex_station: Complex, routes: frozenset[str]) -> str:
        return station_name(
            self.by_complex.get(complex_station.complex_id, ()),
            complex_station.name,
            routes,
        )

    def display(self, complex_station: Complex, routes: frozenset[str]) -> str:
        return f"{self.name(complex_station, routes)} ({','.join(sorted(routes))})"


def haversine(c1: Coord, c2: Coord) -> float:
    """Great-circle metres between two points."""
    r = 6_371_000.0
    p1, p2 = radians(c1.lat), radians(c2.lat)
    dphi = radians(c2.lat - c1.lat)
    dlambda = radians(c2.lon - c1.lon)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlambda / 2) ** 2
    return 2 * r * asin(sqrt(a))


# An index into `WalkPoints.locations`, naming one station -- or the
# centroid of a complex with no station rows of its own, which is the
# only other thing a walk is ever measured from.
# An `int` rather than a type of its own: it is used as a dict key
# hundreds of thousands of times a run, which is the whole point of it,
# and anything wrapping it hashes an order of magnitude slower.
type WalkPointId = int


# No `slots=True`: a slot named `distance` would collide with the method
# of that name below, silently, the slot winning and the method
# disappearing. Nothing is given up for it, there being one of these per
# run: slots are worth having on `ODPair` and `Walk`, of which a
# comparison builds hundreds of thousands, and worth nothing here.
@dataclass(frozen=True, eq=False)
class WalkPoints:
    """Every location a walk can be measured between, by `WalkPointId`.

    Walks run station to station: a rider leaves from whichever of
    their complex's stations is nearest what they are walking to, so a
    complex enters as all of its stations at once, which is what
    `by_complex` holds.

    `eq=False` because a table of coordinates has no meaningful equality
    and no cheap hash: two of them holding the same numbers still aren't
    interchangeable, and a frozen dataclass's generated hash would raise
    on the `list` anyway. `distance`'s cache doesn't key on it -- it
    wraps a bound method, so the table is the closure, not the key.
    """

    locations: list[Coord]
    by_complex: dict[int, tuple[WalkPointId, ...]]
    # Ids below this are stations, in `individual_stations` order;
    # ids at or above it are the centroids standing in for complexes
    # with no station rows of their own.
    n_stations: int

    def __post_init__(self) -> None:
        # Each table remembers its own distances, shadowing the method
        # below with a cached one. `@cache` on the method itself would
        # be a store on the *function*, keyed by `self` and kept for the
        # life of the process, however briefly the table was wanted.
        # `object.__setattr__` because the dataclass is frozen: normal
        # assignment raises, and this is how a frozen one fills in what
        # it derives from its fields.
        object.__setattr__(self, "distance", cache(self.distance))

    def distance(self, point: WalkPointId, other: WalkPointId) -> float:
        """Metres between two of these, remembered per table.

        Ids rather than the `Coord`s themselves, which are dataclasses:
        a dataclass recomputes its hash on every lookup, where an int is
        its own.
        """
        return haversine(self.locations[point], self.locations[other])

    def station(self, point: WalkPointId) -> WalkPointId | None:
        """`point` if it is a station, `None` if it is a centroid."""
        return point if point < self.n_stations else None

    @classmethod
    def build(
        cls, individual_stations: list[Station], stations_by_id: dict[int, Complex]
    ) -> WalkPoints:
        locations = [station.loc for station in individual_stations]
        by_complex: defaultdict[int, list[WalkPointId]] = defaultdict(list)
        for point_id, station in enumerate(individual_stations):
            by_complex[station.complex_id].append(point_id)
        for complex_id, station in stations_by_id.items():
            if complex_id not in by_complex:
                # No station rows of its own, so its centroid stands in,
                # and takes an id past the last station's.
                by_complex[complex_id] = [len(locations)]
                locations.append(station.loc)
        return cls(
            locations=locations,
            by_complex={cid: tuple(ids) for cid, ids in by_complex.items()},
            n_stations=len(individual_stations),
        )


class DayFilterError(Exception):
    """A day filter that selects nothing.

    Raised rather than exiting, so `DayCoverage.query` stays usable as a
    library function; every `analyze` command catches it and exits."""


@dataclass(slots=True, frozen=True)
class DayCoverage:
    """How much of the extract a day filter selects.

    The extract has no dates: every row is already an average over one
    (year, month, day of week), which is why a "day" here is one such group
    and the span is a range of months rather than of dates.
    """

    n_days: int
    first_month: str
    last_month: str

    @classmethod
    def query(
        cls,
        con: duckdb.DuckDBPyConnection,
        parquet: Path,
        day_filter_sql: str,
        day_params: list[str],
    ) -> Self:
        query = f"""
            SELECT COUNT(*), MIN(year_month), MAX(year_month)
            FROM (
                SELECT DISTINCT "Year" * 100 + "Month" AS year_month, "Day of Week"
                FROM read_parquet(?)
                WHERE {day_filter_sql}
            )
        """
        result: tuple[int, int, int] | None = con.execute(
            query, [str(parquet), *day_params]
        ).fetchone()
        assert result is not None, "aggregate query always returns exactly one row"
        n_days, first, last = result
        if not n_days:
            # Before anything divides by it: every command averages its
            # ridership over `n_days`, and `MIN`/`MAX` over no rows are
            # NULL, so an unguarded empty filter is a division by zero
            # or a `None` where a month should be.
            selected = ", ".join(day_params) or "all days"
            raise DayFilterError(
                f"no rows in {parquet} match the day filter ({selected}); "
                f"check --days against the extract's 'Day of Week' values, "
                f"which are full names like 'Monday'"
            )
        return cls(
            n_days=n_days,
            first_month=cls.format_month(first),
            last_month=cls.format_month(last),
        )

    @staticmethod
    def format_month(year_month: int) -> str:
        year, month = divmod(year_month, 100)
        return f"{year}-{month:02d}"
