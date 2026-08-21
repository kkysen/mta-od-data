import csv
from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
from functools import cache
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from typing import Self

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


@dataclass(slots=True, frozen=True)
class Station:
    complex_id: int
    name: str
    routes: frozenset[str]
    loc: Coord
    # "M"/"Bk"/"Bx"/"Q"/"SI", as given by the source data.
    borough: str
    # In Manhattan's Congestion Relief Zone; see `regions.cbd_region`.
    cbd: bool
    # Physical line name (e.g. "4th Av"), per-platform stations only;
    # empty for a complex, which can span several lines.
    line: str = ""

    # B019 warns that caching a method keeps `self` alive forever,
    # but `load_complexes`/`load_individuals` already hold every `Station`
    # for the process's lifetime.
    @cache  # noqa: B019
    def display(self, routes: frozenset[str] | None = None) -> str:
        shown_routes = self.routes if routes is None else routes
        return f"{self.name} ({','.join(sorted(shown_routes))})"

    @classmethod
    def load_complex(cls, row: dict[str, str]) -> Self:
        cid = int(row["complex_id"])
        return cls(
            complex_id=cid,
            name=abbreviate_name(row["stop_name"]),
            routes=frozenset(row["daytime_routes"].split()),
            loc=Coord(lat=float(row["latitude"]), lon=float(row["longitude"])),
            borough=row["borough"],
            cbd=row["cbd"] == "true",
        )

    @classmethod
    def load_complexes(cls, path: Path) -> dict[int, Self]:
        with path.open(newline="") as f:
            return {
                (station := cls.load_complex(row)).complex_id: station
                for row in csv.DictReader(f)
            }

    @classmethod
    def load_individual(cls, row: dict[str, str]) -> Self:
        """Per-platform rows, not complex centroids:
        a merged complex (e.g. Times Sq-42 St/Port Authority Bus Terminal)
        has a centroid that can sit well away from any of its actual
        platforms, which would throw off a nearest-station distance."""
        return cls(
            complex_id=int(row["complex_id"]),
            name=abbreviate_name(row["stop_name"]),
            routes=frozenset(row["daytime_routes"].split()),
            loc=Coord(
                lat=float(row["gtfs_latitude"]), lon=float(row["gtfs_longitude"])
            ),
            borough=row["borough"],
            cbd=row["cbd"] == "true",
            line=row["line"],
        )

    @classmethod
    def load_individuals(cls, path: Path) -> list[Self]:
        with path.open(newline="") as f:
            return [cls.load_individual(row) for row in csv.DictReader(f)]


@cache
def platform_name(
    platforms: tuple[Station, ...], complex_name: str, routes: frozenset[str]
) -> str:
    """`complex_name` narrowed to the platforms `routes` actually stops at.

    A complex's name lists every station merged into it
    ("Chambers St/WTC/Park Pl/Cortlandt St"),
    which is the widest column in most reports
    and mostly about routes the row has nothing to do with.
    The R stops only at Cortlandt St there, so an `(R)` row says that.

    Only when the routes land on exactly one *named* platform.
    Two names means the complex really is the smallest thing
    that covers them
    (Times Sq-42 St and 42 St-Port Authority Bus Terminal, for A,C,N),
    and several platforms sharing one name collapse to it anyway
    (34 St-Herald Sq's 6 Av and Broadway platforms).
    """
    names = {p.name for p in platforms if p.routes & routes}
    return names.pop() if len(names) == 1 else complex_name


@dataclass(slots=True, frozen=True)
class PlatformIndex:
    """Per-platform stations grouped by complex, for `display`."""

    by_complex: dict[int, tuple[Station, ...]]

    @classmethod
    def build(cls, individual_stations: list[Station]) -> Self:
        by_complex: defaultdict[int, list[Station]] = defaultdict(list)
        for station in individual_stations:
            by_complex[station.complex_id].append(station)
        return cls(
            by_complex={cid: tuple(v) for cid, v in by_complex.items()},
        )

    def name(self, station: Station, routes: frozenset[str]) -> str:
        return platform_name(
            self.by_complex.get(station.complex_id, ()), station.name, routes
        )

    def display(self, station: Station, routes: frozenset[str]) -> str:
        return f"{self.name(station, routes)} ({','.join(sorted(routes))})"


@cache
def haversine_m(c1: Coord, c2: Coord) -> float:
    r = 6_371_000.0
    p1, p2 = radians(c1.lat), radians(c2.lat)
    dphi = radians(c2.lat - c1.lat)
    dlambda = radians(c2.lon - c1.lon)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlambda / 2) ** 2
    return 2 * r * asin(sqrt(a))


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
        return cls(
            n_days=n_days,
            first_month=cls.format_month(first),
            last_month=cls.format_month(last),
        )

    @staticmethod
    def format_month(year_month: int) -> str:
        year, month = divmod(year_month, 100)
        return f"{year}-{month:02d}"
