import csv
from dataclasses import dataclass
from enum import StrEnum
from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from typing import Self

from typer import Typer


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
    """Shortened forms for station names that are unwieldy at their full length,
    especially once a route list gets appended in parentheses.
    Applied as a plain substring replacement, so it also shortens compound complex
    names that merge in the long form (e.g. "Chambers St/WTC/Park Place/Cortlandt
    St")."""
    abbreviations = (
        ("Atlantic Av-Barclays Ctr", "Atlantic Av"),
        ("Port Authority Bus Terminal", "PABT"),
        ("Park Place", "Park Pl"),
    )
    for long, short in abbreviations:
        name = name.replace(long, short)
    return name


@dataclass(slots=True)
class Coord:
    lat: float
    lon: float


@dataclass(slots=True)
class Station:
    complex_id: int
    # Base name, without a route list baked in -- callers wanting one call
    # `display()`, either with this station's own full route set (the
    # default) or a narrower one (e.g. just the route(s) a given trip
    # actually used, for a merged complex where those stop at only one of
    # several physical platforms).
    name: str
    routes: set[str]
    loc: Coord
    # "M"/"Bk"/"Bx"/"Q"/"SI", as given by the source data.
    borough: str
    # Whether the station falls in Manhattan's Congestion Relief Zone (below
    # 60th St) -- a curated flag from the source data, not a latitude cut:
    # it correctly excludes Roosevelt Island despite its latitude, and its
    # actual boundary follows 60th St rather than a fixed parallel.
    cbd: bool
    # Physical line name (e.g. "4th Av"), individual per-platform stations
    # only -- empty for a complex, which can span several lines.
    line: str = ""

    def display(self, routes: set[str] | None = None) -> str:
        shown_routes = self.routes if routes is None else routes
        return f"{self.name} ({','.join(sorted(shown_routes))})"

    @classmethod
    def load_complex(cls, row: dict[str, str]) -> Self:
        cid = int(row["complex_id"])
        return cls(
            complex_id=cid,
            name=abbreviate_name(row["stop_name"]),
            routes=set(row["daytime_routes"].split()),
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
        """Per-physical-station rows (not complex centroids). A complex can merge
        several physical stations (e.g. Times Sq-42 St/Port Authority Bus
        Terminal), so its centroid can sit well away from any actual platform;
        these per-station points give accurate nearest-station distances."""
        return cls(
            complex_id=int(row["complex_id"]),
            name=abbreviate_name(row["stop_name"]),
            routes=set(row["daytime_routes"].split()),
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


def haversine_m(c1: Coord, c2: Coord) -> float:
    r = 6_371_000.0
    p1, p2 = radians(c1.lat), radians(c2.lat)
    dphi = radians(c2.lat - c1.lat)
    dlambda = radians(c2.lon - c1.lon)
    a = sin(dphi / 2) ** 2 + cos(p1) * cos(p2) * sin(dlambda / 2) ** 2
    return 2 * r * asin(sqrt(a))


app = Typer()

from mta_od_data.analyze import one_seat_rides  # noqa: E402

app.add_typer(one_seat_rides.app)
