import csv
from collections import defaultdict
from collections.abc import Collection, Hashable
from dataclasses import dataclass, fields
from enum import StrEnum
from functools import cache
from math import asin, cos, radians, sin, sqrt
from operator import attrgetter
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Protocol, Self, override

import duckdb

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


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


@dataclass(slots=True, frozen=True, eq=False)
class HashByField[T: DataclassInstance]:
    """A dataclass wrapped so that it hashes and compares by its fields,
    whatever it does itself.

    For `intern`, whose whole job is to find the object a value is
    already equal to, on types that answer `==` by identity.
    The type is part of the key, so one pool can hold several kinds
    without two of them colliding on equal fields.
    """

    value: T

    @property
    def key(self) -> tuple[type[T], tuple[Hashable, ...]]:
        value = self.value
        # `f.compare`, so this says what the dataclass's own `__eq__`
        # would: a field left out of that is one the type doesn't count
        # as part of what it is, and counting it here would split two
        # values the type calls equal.
        return type(value), tuple(
            getattr(value, f.name) for f in fields(value) if f.compare
        )

    @override
    def __hash__(self) -> int:
        return hash(self.key)

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, HashByField) and self.key == other.key


def intern[T: DataclassInstance](pool: dict[HashByField[T], T], value: T) -> T:
    """`value`, or whatever equal thing was interned before it.

    What lets `Complex` and `Station` be compared by identity: a run
    loads each file once, but nothing stops a second load, and two
    objects of equal value have to be one object for `eq=False` to
    mean what it says.

    By the fields, not by the id: ids are unique only within one
    station file, so keying on them would hand a run with its own
    `--stations` the rows of whichever file was read first.

    Loading is the only way in, so a directly constructed one isn't
    interned; the tests build a few, and never two of equal value.
    """
    return pool.setdefault(HashByField(value), value)


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


# `eq=False` to be hashed and compared by identity, which is what these
# are: `load_all` interns them, one object per complex for the life of a
# run, so two `Complex`es are the same complex exactly when they are the
# same object. A generated `__eq__`/`__hash__` would instead walk every
# field -- a `frozenset` of routes and a `Coord` among them -- on a type
# used as a dict key hundreds of thousands of times a run.
@dataclass(slots=True, frozen=True, eq=False)
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

    # Every `Complex` ever built, by its field values, so that two of
    # them are equal exactly when they are the same object, which is
    # what `eq=False` above assumes. Never emptied, which costs one
    # entry per complex per distinct station file: 445 for the real one.
    _interned: ClassVar[dict[HashByField[Complex], Complex]] = {}

    @classmethod
    def load(cls, row: dict[str, str]) -> Complex:
        complex = cls(
            complex_id=int(row["complex_id"]),
            name=abbreviate_name(row["stop_name"]),
            routes=frozenset(row["daytime_routes"].split()),
            loc=Coord(lat=float(row["latitude"]), lon=float(row["longitude"])),
            borough=row["borough"],
            cbd=row["cbd"] == "true",
        )
        return intern(cls._interned, complex)

    @classmethod
    def load_all(cls, path: Path) -> dict[int, Complex]:
        """By id, which is also what interns them:
        one object per complex for the process's lifetime,
        so a `Station` can hold its own rather than an id to look up.
        """
        with path.open(newline="") as f:
            return {
                (complex := cls.load(row)).complex_id: complex
                for row in csv.DictReader(f)
            }


# By identity, like `Complex`, and for the same reason: `Station.load_all`
# builds one object per row of the reference data, and nothing else
# constructs one. Field-wise hashing would be worse here than there,
# since a `Station` holds its `Complex` and would hash that too.
@dataclass(slots=True, frozen=True, eq=False)
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

    _interned: ClassVar[dict[HashByField[Station], Station]] = {}

    @classmethod
    def load(cls, row: dict[str, str], complexes: dict[int, Complex]) -> Station:
        station = cls(
            complex=complexes[int(row["complex_id"])],
            name=abbreviate_name(row["stop_name"]),
            routes=frozenset(row["daytime_routes"].split()),
            loc=Coord(
                lat=float(row["gtfs_latitude"]), lon=float(row["gtfs_longitude"])
            ),
            line=row["line"],
            station_id=int(row["station_id"]),
        )
        # Its `complex` is interned too, so it keys by identity here.
        return intern(cls._interned, station)

    @classmethod
    def load_all(cls, path: Path, complexes: dict[int, Complex]) -> list[Station]:
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


def haversine(c1: Coord, c2: Coord) -> float:
    """Great-circle metres between two points."""
    r = 6_371_000.0
    p1, p2 = radians(c1.lat), radians(c2.lat)
    dphi = radians(c2.lat - c1.lat)
    dlambda = radians(c2.lon - c1.lon)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlambda / 2) ** 2
    return 2 * r * asin(sqrt(a))


# No `slots=True`: a slot named `distance` would collide with the method
# of that name below, silently, the slot winning and the method
# disappearing. Nothing is given up for it, there being one of these per
# run: slots are worth having on `ODPair` and `Walk`, of which a
# comparison builds hundreds of thousands, and worth nothing here.
#
# `eq=False` because a table of stations has no meaningful equality and
# no cheap hash: two of them holding the same stations still aren't
# interchangeable, and a frozen dataclass's generated hash would raise
# on the `dict` anyway. `distance`'s cache doesn't key on it -- it wraps
# a bound method, so the table is the closure, not the key.
@dataclass(frozen=True, eq=False)
class ComplexStations:
    """The `Station`s in each complex: what a complex reads as, and
    what a walk to or from it is measured between.

    The two go together because they are the same question asked twice.
    A complex is several stations, so naming one means narrowing to the
    stations a route set reaches, and walking to one means reaching
    whichever of its stations is nearest: a rider bound for Times Sq on
    the N,Q,R is on its Broadway station both for what the row calls it
    and for how far they walk.
    """

    by_complex: dict[Complex, tuple[Station, ...]]

    def __post_init__(self) -> None:
        # Each table remembers its own distances, shadowing the method
        # below with a cached one. `@cache` on the method itself would
        # be a store on the *function*, keyed by `self` and kept for the
        # life of the process, however briefly the table was wanted.
        # `object.__setattr__` because the dataclass is frozen: normal
        # assignment raises, and this is how a frozen one fills in what
        # it derives from its fields.
        object.__setattr__(self, "distance", cache(self.distance))

    def distance(self, station: Station, other: Station) -> float:
        """Metres between two stations, remembered per table.

        The stations themselves, which is affordable because they are
        interned and so hash by identity: hashing one by its fields
        would cost more than the `haversine` this is caching.
        """
        return haversine(station.loc, other.loc)

    def name(self, complex: Complex, routes: frozenset[str]) -> str:
        return station_name(self.by_complex.get(complex, ()), complex.name, routes)

    def display(self, complex: Complex, routes: frozenset[str]) -> str:
        return f"{self.name(complex, routes)} ({','.join(sorted(routes))})"

    @classmethod
    def build(
        cls, individual_stations: list[Station], complexes: Collection[Complex]
    ) -> ComplexStations:
        by_complex: defaultdict[Complex, list[Station]] = defaultdict(list)
        for station in individual_stations:
            by_complex[station.complex].append(station)
        # Every one of the 445 real complexes has stations of its own,
        # and a walk is only ever measured between stations, so a
        # complex without any is a station file this can't answer for.
        # It used to fall back to the complex's centroid, silently
        # measuring to a point no rider stands at.
        without = sorted(set(complexes) - set(by_complex), key=attrgetter("complex_id"))
        if without:
            raise ValueError(
                f"{len(without)} complexes have no stations of their own "
                f"({[c.name for c in without[:5]]}...): a walk is measured "
                "between stations, so there is nowhere to measure from"
            )
        return cls(by_complex={c: tuple(v) for c, v in by_complex.items()})


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
