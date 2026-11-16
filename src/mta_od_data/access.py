"""
How long it takes to get between the street and the platforms
through each station entrance,
for changing trains between stations on the streets:
climbing or riding the station's depth or height, and through the fare gates,
in `secs`.
`raptor` adds the walk along the platform, at `raptor/assign.json5`'s speeds:
in, none, as riders board right where the stairs reach the platform;
out, the average from riders' spots along the train to the stairs,
some planning their car to be near them and the rest anywhere (`cars`),
as for changing trains on a platform.
Where the stairs reach the platform is taken as `platform_ft` from its middle,
the station's GTFS coordinate, in a straight line from the entrance,
or its end if that's farther than half the platform,
and the rest is a corridor walked both ways.
The platform's length is the longest of the station's platforms OpenStreetMap outlines,
or else a full-length train's: 600 ft in the B Division, 510 ft in the A (IRT).

The depth comes from, in order:
the heights of the MTA's elevators and escalators,
depths published elsewhere for the few deep stations the MTA leaves blank (`DEPTHS`),
the levels OpenStreetMap puts the station's platforms on,
in feet as the MTA's heights fit them,
and last the station's structure.

Moved from `subway-sheds`, as it was there but for its planned stations,
and since walking along the platform too.

OSM's platforms are read from Geofabrik's New York extract
(`platforms.DEFAULT_EXTRACT`),
each station's as `platforms.csv` matches them to its stops.
"""

import json
import re
from collections import defaultdict
from csv import DictReader, DictWriter
from dataclasses import dataclass
from math import cos, hypot, isnan, nan, radians
from pathlib import Path
from statistics import median
from typing import Annotated, Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import osmium
from osmium.osm import Node, Way
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import CACHE
from mta_od_data.platforms import DEFAULT_EXTRACT
from mta_od_data.platforms import DEFAULT_OUT as DEFAULT_PLATFORMS
from mta_od_data.prepare import DEFAULT_STATIONS_CSV

app = Typer()

DIR = CACHE / "access"
# The MTA's open data: every subway entrance, and every elevator and escalator.
ENTRANCES_URL = "https://data.ny.gov/resource/i9wp-a4ja.csv?$limit=10000"
LIFTS_URL = "https://data.ny.gov/resource/94fv-bak7.csv?$limit=10000"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
# Subway platforms and their levels, over the city.
OVERPASS_QUERY = """[out:json][timeout:120];
(nwr["railway"="platform"](40.49,-74.27,40.92,-73.68);
 nwr["public_transport"="platform"]["subway"="yes"](40.49,-74.27,40.92,-73.68););
out tags center;"""

# What routing reads: committed,
# so that what the MTA or OSM change doesn't change routing
# until it's rebuilt and reviewed.
TABLE = DATA / "station_access.csv"
COLUMNS = [
    "station",
    "complex",
    "name",
    "lat",
    "lon",
    "kind",
    "depth_ft",
    "depth_source",
    "platform_ft",
    "length_ft",
    "length_source",
    "secs",
]

# Stairs, about 1 ft a second up or down, averaged: Fruin's walking speeds on stairs,
# about 0.5 to 0.6 m/s along a 7 in riser's slope.
STAIRS_FT_PER_S = 1.0
# Escalators at the 100 ft a minute that US code allows and NYC's run at,
# riders standing,
# half of it upwards on a 30 degree incline.
ESCALATOR_FT_PER_S = 100 / 60 / 2
# Elevators: half a minute's wait, as if they came every minute,
# the doors, and the ride.
ELEVATOR_WAIT_S = 30
ELEVATOR_DOORS_S = 10
ELEVATOR_FT_PER_S = 2.0
# Through the fare gates and across to the stairs, once each way in or out.
GATES_S = 15
# Deeper than this, no one takes stairs: the station's escalators or elevators instead.
DEEP_FT = 60
# The walking speed of the street walks, for the long walks inside a station (`WALKS`).
WALK_FT_PER_S = 3 * 5280 / 3600
# A platform's length where OSM outlines none of the station's:
# a full-length train's, ten 60 ft cars in the B Division
# and ten 51 ft cars in the A, the IRT's,
# and the B Division's on the Staten Island Railway.
B_DIVISION_FT = 600
A_DIVISION_FT = 510

# Depths the MTA's heights leave blank, as published, in feet to the platform.
DEPTHS = {
    # https://en.wikipedia.org/wiki/72nd_Street_station_(Second_Avenue_Subway),
    # https://subwaynut.com/second_ave_subway/72_street/index.php
    "Q03": (99.0, "about 99 ft: Wikipedia, subwaynut"),
    # The upper level, toward Manhattan, about 140 ft,
    # the lower, toward Queens, about 155:
    # https://en.wikipedia.org/wiki/Lexington_Avenue%E2%80%9363rd_Street_station
    "B08": (148.0, "140 and 155 ft levels: Wikipedia"),
    # https://en.wikipedia.org/wiki/190th_Street_station,
    # https://untappedcities.com/deepest-highest-subway-stations-nyc
    "A05": (140.0, "about 140 ft: Wikipedia, Untapped Cities"),
}


@dataclass(frozen=True, slots=True)
class Walk:
    """An entrance reached by a level walk inside the station before its climb."""

    feet: float
    climb_ft: float
    note: str


# Complexes changed between without leaving the system,
# which the MTA lists as separate, each by the one it's joined to:
# 42 St-Bryant Pk and 5 Av's, by the passage to Times Sq-42 St's.
JOINED_COMPLEXES = {"609": "611"}

# Entrances the MTA lists under the wrong station, by station and coordinates:
# 86 St's (R) at 78 St, 870 m from its platforms and 80 m from 77 St's.
WRONG_ENTRANCES = {("R44", 40.6302302, -74.0254577)}

# Entrances reached by a long walk inside the station,
# by the MTA's entrance coordinates.
WALKS = {
    # 191 St's Broadway entrance: OSM's "Tunnel Street" footway, 280 m,
    # to the elevators under St Nicholas Ave,
    # whose top is 66.8 m up by NYC's 2017 LiDAR ground model, to the entrance's 23.7 m,
    # so with the elevators' 173 ft the platform is about 32 ft below the entrance.
    (40.856413, -73.932605): Walk(280 / 0.3048, 32, "Broadway tunnel, 280 m"),
}

# Each structure's depth or height where nothing else gives it.
STRUCTURE_FT = {
    "Subway": 25,
    "Elevated": 30,
    "Viaduct": 30,
    "Embankment": 15,
    "Open Cut": 20,
    "At Grade": 0,
}


def _download(url: str, dest: Path, data: dict[str, str] | None = None) -> Path:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        body = urlencode(data).encode() if data else None
        request = Request(url, data=body, headers={"User-Agent": "mta-od-data"})
        with urlopen(request, timeout=180) as response:
            dest.write_bytes(response.read())
    return dest


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(DictReader(f))


def feet(text: str) -> float:
    """A height the MTA gives as `172’9”`, `103'-5in`, or `15824 mm (51'-11in)`,
    in feet."""
    if m := re.search(r"([\d,]+)\s*mm", text):
        return int(m[1].replace(",", "")) / 304.8
    m = re.match(r"\s*(\d+)\s*(?:'|’|ft)?\s*-?\s*(\d+)?", text)
    if not m:
        return nan
    return int(m[1]) + int(m[2] or 0) / 12


def _max(values: list[float]) -> float:
    """The largest of `values` that aren't NaN, or NaN if none."""
    values = [v for v in values if not isnan(v)]
    return max(values) if values else nan


@dataclass(frozen=True, slots=True)
class Lift:
    rise: float
    street: bool


@dataclass(frozen=True, slots=True)
class LiftDepths:
    """A station's depth or height by its elevators' and escalators' heights."""

    elevator_ft: float
    escalator_ft: float
    has_escalators: bool


def _chain(lifts: list[Lift]) -> float:
    """
    Elevators side by side, so the tallest,
    or the tallest from the street and then to the platform;
    escalators one after another, from the street and then down further,
    as at Hudson Yards.
    """
    tallest = _max([lift.rise for lift in lifts])
    if isnan(tallest):
        return nan
    top = _max([lift.rise for lift in lifts if lift.street])
    rest = _max([lift.rise for lift in lifts if not lift.street])
    return max(tallest, (0 if isnan(top) else top) + (0 if isnan(rest) else rest))


def lift_depths(lifts: list[dict[str, str]]) -> dict[str, LiftDepths]:
    """Each station's `LiftDepths`, by MTA station ID."""
    by_station: dict[str, tuple[list[Lift], list[Lift]]] = {}
    for row in lifts:
        rise = row["elevator_rise"] or row["escalator_rise"]
        lift = Lift(feet(rise) if rise else nan, row["street_access"] == "YES")
        elevators, escalators = by_station.setdefault(
            row["station_mrn"].lstrip("0"), ([], [])
        )
        match row["elevator_or_escalator"]:
            case "Elevator":
                elevators.append(lift)
            case "Escalator":
                escalators.append(lift)
    return {
        station: LiftDepths(
            elevator_ft=_chain(elevators) if elevators else nan,
            escalator_ft=_chain(escalators) if escalators else nan,
            has_escalators=bool(escalators),
        )
        for station, (elevators, escalators) in by_station.items()
    }


def osm_levels(stations: list[dict[str, str]], osm: dict[str, Any]) -> list[float]:
    """The level of the platform OSM puts nearest each station, within 150 m."""
    platforms = []
    for element in osm["elements"]:
        tags = element.get("tags", {})
        center = element.get("center", element)
        if "level" in tags and "lat" in center:
            try:
                level = float(tags["level"].split(";")[0])
            except ValueError:
                continue
            platforms.append((center["lat"], center["lon"], level))

    def nearest(lat: float, lon: float) -> float:
        best = (150.0, nan)
        for plat, plon, level in platforms:
            dy = (plat - lat) * 111_111
            dx = (plon - lon) * 111_111 * cos(radians(lat))
            best = min(best, (hypot(dx, dy), level))
        return best[1]

    return [
        nearest(float(s["gtfs_latitude"]), float(s["gtfs_longitude"])) for s in stations
    ]


def platform_ft(station: dict[str, str], lat: float, lon: float) -> float:
    """How far an entrance at `lat`, `lon` is along the platforms from their middle,
    the station's GTFS coordinate, in a straight line."""
    slat = float(station["gtfs_latitude"])
    slon = float(station["gtfs_longitude"])
    dy = (lat - slat) * 111_111
    dx = (lon - slon) * 111_111 * cos(radians(slat))
    return hypot(dx, dy) * 3.28084


class _WayNodes(osmium.SimpleHandler):
    """Each wanted way's nodes, by their IDs."""

    def __init__(self, ways: set[int]) -> None:
        super().__init__()
        self.ways = ways
        self.nodes: dict[str, list[int]] = {}

    def way(self, w: Way) -> None:
        if w.id in self.ways:
            self.nodes[f"w{w.id}"] = [n.ref for n in w.nodes]


class _NodeLocations(osmium.SimpleHandler):
    """Each wanted node's `(lon, lat)`."""

    def __init__(self, nodes: set[int]) -> None:
        super().__init__()
        self.wanted = nodes
        self.at: dict[int, tuple[float, float]] = {}

    def node(self, n: Node) -> None:
        if n.id in self.wanted:
            self.at[n.id] = (n.location.lon, n.location.lat)


def osm_lengths(
    extract: Path = DEFAULT_EXTRACT, platforms: Path = DEFAULT_PLATFORMS
) -> dict[str, tuple[float, str]]:
    """The length of each station's longest platform OSM outlines, in feet,
    and its way, by GTFS stop ID.

    The extract is read twice, for the ways' nodes and then their locations,
    not with every node's location at hand, which takes over a gigabyte.
    """
    # `lidar` reads this module's table.
    from mta_od_data.lidar import PlatformAxis, ground_outline

    ways: dict[str, set[str]] = defaultdict(set)
    for r in _rows(platforms):
        if r["platform"].startswith("w"):
            ways[r["stop"]].add(r["platform"])
    wanted = {int(w[1:]) for ws in ways.values() for w in ws}
    way_nodes = _WayNodes(wanted)
    way_nodes.apply_file(str(extract))
    locations = _NodeLocations({n for ns in way_nodes.nodes.values() for n in ns})
    locations.apply_file(str(extract))
    feet = {}
    for way, nodes in way_nodes.nodes.items():
        outline = [locations.at[n] for n in nodes if n in locations.at]
        # Outlined, not mapped as a line or with nodes missing.
        if len(outline) == len(nodes) > 3 and nodes[0] == nodes[-1]:
            axis = PlatformAxis.of(ground_outline(outline, outline[0]))
            feet[way] = axis.length / 0.3048
    return {
        stop: max((feet[w], w) for w in ws if w in feet)
        for stop, ws in ways.items()
        if any(w in feet for w in ws)
    }


def platform_length(
    station: dict[str, str], osm: dict[str, tuple[float, str]]
) -> tuple[float, str]:
    """The station's platform length in feet, from OSM's `osm_lengths` if it has it,
    or else a full-length train's in its division, and where it's from."""
    if station["gtfs_stop_id"] in osm:
        ft, way = osm[station["gtfs_stop_id"]]
        return ft, f"OSM {way}"
    match station["division"]:
        case "IRT":
            return A_DIVISION_FT, "A Division train"
        case "SIR":
            # Its route relations aren't the NYC Subway's, so `platforms.csv` has none.
            return B_DIVISION_FT, "SIR, as a B Division train"
        case _:
            return B_DIVISION_FT, "B Division train"


def entrance_secs(
    kind: str, depth_ft: float, has_escalators: bool, walk: Walk | None
) -> float:
    """Seconds between the street and where the stairs reach the platform
    through an entrance of `kind`,
    or to the platform's middle through a long walk inside the station."""
    if walk is not None:
        return walk.feet / WALK_FT_PER_S + walk.climb_ft / STAIRS_FT_PER_S + GATES_S
    return _climb_secs(kind, depth_ft, has_escalators)


def _climb_secs(kind: str, depth_ft: float, has_escalators: bool) -> float:
    if "Elevator" in kind or (depth_ft > DEEP_FT and not has_escalators):
        return (
            ELEVATOR_WAIT_S + ELEVATOR_DOORS_S + depth_ft / ELEVATOR_FT_PER_S + GATES_S
        )
    if "Escalator" in kind or depth_ft > DEEP_FT:
        return depth_ft / ESCALATOR_FT_PER_S + GATES_S
    return depth_ft / STAIRS_FT_PER_S + GATES_S


@dataclass(frozen=True, slots=True)
class Depth:
    """A station's depth or height, and what it's from."""

    station: dict[str, str]
    ft: float
    source: str
    has_escalators: bool


def depths(
    stations: list[dict[str, str]], lifts: dict[str, LiftDepths], osm: dict[str, Any]
) -> dict[str, Depth]:
    """Each station's `Depth`, by GTFS stop ID."""
    levels = osm_levels(stations, osm)
    none = LiftDepths(nan, nan, has_escalators=False)
    by_lifts = [lifts.get(s["station_id"], none) for s in stations]
    mta_ft = [_max([d.elevator_ft, d.escalator_ft]) for d in by_lifts]
    # Feet a level, as the MTA's heights fit OSM's levels where both have a station.
    ft_per_level = median(
        ft / abs(level)
        for ft, level in zip(mta_ft, levels, strict=True)
        if not isnan(ft) and not isnan(level) and level != 0
    )

    def depth(
        station: dict[str, str], mta_ft: float, level: float
    ) -> tuple[float, str]:
        if station["gtfs_stop_id"] in DEPTHS:
            return DEPTHS[station["gtfs_stop_id"]]
        if not isnan(mta_ft):
            return mta_ft, "MTA elevators and escalators"
        if not isnan(level) and level != 0:
            return abs(level) * ft_per_level, f"OSM level {level:g}"
        return STRUCTURE_FT.get(
            station["structure"], 25
        ), f"structure {station['structure']}"

    out = {}
    for station, d, ft, level in zip(stations, by_lifts, mta_ft, levels, strict=True):
        depth_ft, source = depth(station, ft, level)
        out.setdefault(
            station["gtfs_stop_id"],
            Depth(station, float(depth_ft), source, d.has_escalators),
        )
    return out


def build(
    stations_csv: Path = DEFAULT_STATIONS_CSV, extract: Path = DEFAULT_EXTRACT
) -> list[dict[str, object]]:
    """Every entrance's time between the street and its station's platforms,
    without the walk along them."""
    entrances = _rows(_download(ENTRANCES_URL, DIR / "entrances.csv"))
    lifts = lift_depths(_rows(_download(LIFTS_URL, DIR / "lifts.csv")))
    osm = json.loads(
        _download(
            OVERPASS_URL, DIR / "platforms.json", {"data": OVERPASS_QUERY}
        ).read_text()
    )
    by_id = depths(_rows(stations_csv), lifts, osm)
    lengths = osm_lengths(extract)

    def row(gtfs_id: str, lat: float, lon: float, kind: str) -> dict[str, object]:
        depth = by_id[gtfs_id]
        complex_id = depth.station["complex_id"]
        walk = WALKS.get((lat, lon))
        along = 0.0 if walk else platform_ft(depth.station, lat, lon)
        # Blank for a long walk inside the station, timed to the platform's middle.
        length = None if walk else platform_length(depth.station, lengths)
        return {
            "station": gtfs_id,
            "complex": JOINED_COMPLEXES.get(complex_id, complex_id),
            "name": depth.station["stop_name"],
            "lat": lat,
            "lon": lon,
            "kind": kind,
            "depth_ft": round(depth.ft, 1),
            "depth_source": walk.note if walk else depth.source,
            "platform_ft": round(along),
            "length_ft": "" if length is None else round(length[0]),
            "length_source": "" if length is None else length[1],
            "secs": round(entrance_secs(kind, depth.ft, depth.has_escalators, walk)),
        }

    rows = [
        row(
            gtfs_id,
            float(e["entrance_latitude"]),
            float(e["entrance_longitude"]),
            e["entrance_type"],
        )
        for e in entrances
        if "YES" in (e["entry_allowed"], e["exit_allowed"])
        # An entrance a complex's stations share lists each of them.
        for gtfs_id in e["gtfs_stop_id"].split("; ")
        if (
            gtfs_id,
            float(e["entrance_latitude"]),
            float(e["entrance_longitude"]),
        )
        not in WRONG_ENTRANCES
    ]
    rows = _drop_misattributed(rows)
    # Stations the MTA lists no entrances for, at their own coordinates.
    listed = {r["station"] for r in rows}
    rows += [
        row(
            gtfs_id,
            float(d.station["gtfs_latitude"]),
            float(d.station["gtfs_longitude"]),
            "Station",
        )
        for gtfs_id, d in by_id.items()
        if gtfs_id not in listed
    ]
    return rows


STREET = "Easement - Street"


def _drop_misattributed(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """`rows` without street entrances the MTA lists
    under stations not connected to each other.

    The MTA lists some entrances under stations of different complexes.
    A station house or passage may really join them, as at Fulton St,
    but it lists a street entrance at Broadway under both 50 Sts,
    the 1's and the C and E's at 8 Av,
    and one near William St under both Wall Sts and Broad St,
    so routing changed between them through it in barely more than going in and out.
    Stations are connected if in one complex or sharing a station house or passage,
    and a street entrance listed under stations not all connected
    is dropped from all of them,
    as there's no telling whose it is.
    """
    complexes: dict[tuple[object, object], set[object]] = {}
    joining: dict[tuple[object, object], set[object]] = {}
    for r in rows:
        place = (r["lat"], r["lon"])
        complexes.setdefault(place, set()).add(r["complex"])
        if r["kind"] != STREET:
            joining.setdefault(place, set()).add(r["complex"])
    connected = {
        frozenset((a, b))
        for joined in joining.values()
        for a in joined
        for b in joined
        if a != b
    }
    unconnected = {
        place
        for place, listed in complexes.items()
        if any(
            frozenset((a, b)) not in connected
            for a in listed
            for b in listed
            if str(a) < str(b)
        )
    }
    return [
        r
        for r in rows
        if not (r["kind"] == STREET and (r["lat"], r["lon"]) in unconnected)
    ]


@app.command()
def fetch_station_access(
    stations: Annotated[
        Path, Option(help="The station reference CSV")
    ] = DEFAULT_STATIONS_CSV,
    extract: Annotated[
        Path, Option(help="Geofabrik's New York extract, for OSM's platforms")
    ] = DEFAULT_EXTRACT,
) -> None:
    """
    Rebuild each station entrance's time to the platforms, `data/station_access.csv`,
    from the MTA's and OSM's data now, to review and commit.
    """
    rows = build(stations, extract)
    TABLE.parent.mkdir(parents=True, exist_ok=True)
    with TABLE.open("w", newline="") as f:
        out = DictWriter(f, COLUMNS, lineterminator="\n")
        out.writeheader()
        out.writerows(rows)
    print(f"{len(rows)} entrances of {len({r['station'] for r in rows})} stations")
