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
The platform's length is that of the edge of the platform OpenStreetMap outlines
where a stop's trains stop, each direction's its own,
as an island's two edges differ where it curves,
measured along the edge, so a curved one along the curve,
and whole where OSM maps the platform in pieces, as Morris Park's.
Each GTFS stop's edge, by direction and platform, is in `platform_edges.csv`,
and each entrance's `length_ft` is the station's longest,
for its stops whose platform isn't known.
Where OSM outlines none of the station's platforms, it's a full-length train's:
600 ft in the B Division, 510 ft in the A (IRT),
and 300 ft on the Staten Island Railway, whose trains are half as long.

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
from collections import Counter, defaultdict
from csv import DictReader, DictWriter
from dataclasses import dataclass
from functools import cached_property
from itertools import pairwise
from math import atan2, cos, hypot, isnan, nan, pi, radians
from pathlib import Path
from statistics import median
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import osmium
from osmium.osm import Node, Way
from shapely import (
    LineString,
    MultiPolygon,
    Point,
    Polygon,
    get_coordinates,
    unary_union,
)
from shapely.ops import nearest_points, substring
from typer import Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import CACHE
from mta_od_data.downloads import stations_csv as fetch_stations
from mta_od_data.platforms import DEFAULT_EXTRACT, Relations, fetch_extract
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
# Each stop's edge, by direction and platform, beside it, as `raptor` reads it.
EDGES = TABLE.with_name("platform_edges.csv")
EDGE_COLUMNS = ["stop", "platform", "length_ft"]
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
# and ten 51 ft cars in the A, the IRT's;
# the Staten Island Railway's trains are half a B Division one.
B_DIVISION_FT = 600
A_DIVISION_FT = 510
SIR_FT = 300
# The ways OSM maps a platform's trains' tracks as.
TRACKS = {"subway", "rail", "light_rail"}
# How far a track beside a platform is from its outline, at most, in metres:
# a train's side is about 1.6 m from its track's middle,
# with room for OSM's tracks and outlines being a little off.
BESIDE_M = 6.0
# How much farther from a track than its nearest corner
# a platform's corners along its track edge can be, in metres,
# as where OSM draws the edge a little crooked.
EDGE_M = 2.0
# How far past a platform's ends its track is followed, in metres.
PAST_M = 50.0
# How far a track is run on straight past where OSM's ends,
# as at a terminal's bumpers, in metres.
RUN_ON_M = 100.0
# The sharpest a track turns at one node, in degrees:
# sharper is another track crossing it, or a way doubling back.
MAX_TURN_DEG = 30.0

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


class _PlatformWays(Relations):
    """Every platform OSM outlines: its nodes, by its way's ID,
    and its name and level, by which its pieces are told apart from other platforms;
    the tracks: the nodes each track node is joined to;
    and the NYC Subway's route relations, whose stops are on the tracks they stop on."""

    def __init__(self) -> None:
        super().__init__()
        self.nodes: dict[str, list[int]] = {}
        self.named: dict[str, tuple[str, str]] = {}
        self.joined: dict[int, set[int]] = defaultdict(set)

    def way(self, w: Way) -> None:
        railway = w.tags.get("railway")
        if railway == "platform":
            way = f"w{w.id}"
            self.nodes[way] = [n.ref for n in w.nodes]
            self.named[way] = (w.tags.get("name") or "", w.tags.get("level") or "")
        elif railway in TRACKS:
            nodes = [n.ref for n in w.nodes]
            for a, b in pairwise(nodes):
                self.joined[a].add(b)
                self.joined[b].add(a)

    @cached_property
    def by_node(self) -> dict[int, set[str]]:
        """The platforms each node outlines."""
        by_node: dict[int, set[str]] = defaultdict(set)
        for w, nodes in self.nodes.items():
            for n in nodes:
                by_node[n].add(w)
        return by_node

    def pieces(self, way: str) -> set[str]:
        """The way, and the platform's other pieces, joined to it node to node.

        OSM splits some platforms where they change from tunnel to embankment to bridge,
        as at Morris Park, so the way `platforms.csv` matches is only part of it.
        """
        found = {way}
        todo = [way]
        while todo:
            for n in self.nodes[todo.pop()]:
                for w in self.by_node[n] - found:
                    if self.named[w] == self.named[way]:
                        found.add(w)
                        todo.append(w)
        return found


class _NodeLocations(osmium.SimpleHandler):
    """Each wanted node's `(lon, lat)`."""

    def __init__(self, nodes: set[int]) -> None:
        super().__init__()
        self.wanted = nodes
        self.at: dict[int, tuple[float, float]] = {}

    def node(self, n: Node) -> None:
        if n.id in self.wanted:
            self.at[n.id] = (n.location.lon, n.location.lat)


@dataclass(frozen=True, slots=True)
class Tracks:
    """Track nodes, at metres east and north of a platform,
    and the nodes each is joined to by a track."""

    at: dict[int, tuple[float, float]]
    joined: dict[int, set[int]]


@dataclass(frozen=True, slots=True)
class TrackEdge:
    """A platform's edge where trains stop: its length in metres,
    and the track beside it, as OSM maps it."""

    metres: float
    track: LineString


def track_edges(outline: Polygon | MultiPolygon, tracks: Tracks) -> list[TrackEdge]:
    """A platform's edges where trains stop, measured along their tracks:
    a side platform's one, an island's two, which differ where it curves;
    none if no track runs beside it.

    Each track beside the platform is followed on past both its ends,
    and the platform's edge along it is measured along it.
    A track beyond another, as an express track past a side platform's local,
    isn't beside it.
    The ends are measured, not the outline between them,
    so a jagged or notched outline measures as a smooth one,
    and a platform OSM outlines with a few corners as on the curve its track takes.
    """
    besides = sorted(
        (d, a, b)
        for a in tracks.at
        for b in tracks.joined.get(a, set())
        if a < b
        and b in tracks.at
        # Beside it, not under or over it.
        and 0
        < (d := LineString([tracks.at[a], tracks.at[b]]).distance(outline))
        <= BESIDE_M
    )
    lines: list[LineString] = []
    for d, a, b in besides:
        middle = LineString([tracks.at[a], tracks.at[b]]).interpolate(
            0.5, normalized=True
        )
        # Each track once, from its stretch nearest the platform.
        if all(line.distance(middle) > 1 for line in lines):
            lines.append(_follow(tracks, (a, b), outline, d))
    # As OSM maps them, not run on.
    mapped = [LineString(line.coords[1:-1]) for line in lines]

    def beyond(line: LineString, across: LineString) -> bool:
        """Whether another track is between `line` and the platform:
        tracks side by side are about 3.5 m apart or more, middle to middle,
        so a track nearer than half that is one joining it at a switch."""
        return any(
            other is not line
            and across.intersects(track)
            and across.intersection(track).distance(Point(across.coords[0])) > 1.75
            for other, track in zip(lines, mapped, strict=True)
        )

    return [
        TrackEdge(edge[0], track)
        for line, track in zip(lines, mapped, strict=True)
        if (edge := _edge(outline, line)) and not beyond(line, edge[1])
    ]


def _turn(
    a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]
) -> float:
    """How far a track from `a` to `b` turns at `b` toward `c`,
    in radians, left positive."""
    t = atan2(c[1] - b[1], c[0] - b[0]) - atan2(b[1] - a[1], b[0] - a[0])
    return (t + pi) % (2 * pi) - pi


def _follow(
    tracks: Tracks, start: tuple[int, int], outline: Polygon | MultiPolygon, d: float
) -> LineString:
    """The track through `start`, a stretch `d` from the platform,
    on past its ends, or run on straight past where OSM's track ends.

    Where tracks fork beside the platform, it keeps to the one as far from it;
    past it, to the straighter.
    """
    at = tracks.at

    def apart(a: int, b: int) -> float:
        return (
            LineString([at[a], at[b]])
            .interpolate(0.5, normalized=True)
            .distance(outline)
        )

    def onward(path: list[int]) -> None:
        while Point(at[path[-1]]).distance(outline) <= PAST_M:
            prev, here = path[-2], path[-1]
            ahead = [
                n
                for n in tracks.joined.get(here, set())
                if n in at
                and n not in path
                and abs(_turn(at[prev], at[here], at[n])) < radians(MAX_TURN_DEG)
            ]
            if not ahead:
                return
            beside = [n for n in ahead if apart(here, n) <= d + EDGE_M]
            path.append(
                min(beside, key=lambda n: abs(apart(here, n) - d))
                if beside
                else min(ahead, key=lambda n: abs(_turn(at[prev], at[here], at[n])))
            )

    path = list(start)
    onward(path)
    path.reverse()
    onward(path)
    points = [at[n] for n in path]

    def run_on(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float]:
        k = RUN_ON_M / hypot(b[0] - a[0], b[1] - a[1])
        return (b[0] + (b[0] - a[0]) * k, b[1] + (b[1] - a[1]) * k)

    return LineString(
        [run_on(points[1], points[0]), *points, run_on(points[-2], points[-1])]
    )


def _edge(
    outline: Polygon | MultiPolygon, track: LineString
) -> tuple[float, LineString] | None:
    """The length of the platform's edge along `track`, in metres,
    and the way across from the track to it at its middle,
    or `None` if the track only touches it.

    The edge's corners are those the track faces across no platform,
    or as near it as its nearest, within `EDGE_M`,
    and it runs between the two farthest apart along the track.
    It's as long as the track between them,
    less its distance from the track for each radian the track turns toward it,
    or more, turning away.
    """
    corners = [Point(c) for c in get_coordinates(outline)]
    apart = [track.distance(c) for c in corners]
    nearest = min(apart)

    def faces(c: Point) -> bool:
        foot = track.interpolate(track.project(c))
        return LineString([c, foot]).intersection(outline).length < 0.05

    edge = [
        (track.project(c), d)
        for c, d in zip(corners, apart, strict=True)
        if d <= nearest + EDGE_M or faces(c)
    ]
    start = min(s for s, _ in edge)
    end = max(s for s, _ in edge)
    if end - start < 1:
        return None
    bends = [
        (float(x), float(y)) for x, y in get_coordinates(substring(track, start, end))
    ]
    # Without a corner twice over, which turns no way.
    bends = bends[:1] + [b for a, b in pairwise(bends) if b != a]
    turns = sum(
        _turn(a, b, c) for a, b, c in zip(bends, bends[1:], bends[2:], strict=False)
    )
    # Which side of the track the platform is, at the edge's middle.
    middle = track.interpolate((start + end) / 2)
    ahead = track.interpolate((start + end) / 2 + 1)
    _, toward = nearest_points(middle, outline)
    left = (ahead.x - middle.x) * (toward.y - middle.y) > (ahead.y - middle.y) * (
        toward.x - middle.x
    )
    offset = median(d for _, d in edge)
    return (
        end - start - (1 if left else -1) * offset * turns,
        LineString([middle, toward]),
    )


@dataclass(frozen=True, slots=True)
class OsmLengths:
    """OSM's platform lengths, in feet.

    `longest`: each station's longest edge where trains stop, and its platform's way,
    by GTFS stop ID, for its stops whose platform isn't known.
    `edges`: the length of the edge each direction's trains stop at
    on each of its platforms,
    by GTFS stop, as `127N`, and platform way.
    """

    longest: dict[str, tuple[float, str]]
    edges: dict[tuple[str, str], float]


def osm_lengths(
    extract: Path = DEFAULT_EXTRACT,
    platforms: Path = DEFAULT_PLATFORMS,
    stations: Path = DEFAULT_STATIONS_CSV,
) -> OsmLengths:
    """The length of each platform OSM outlines, along each of its edges,
    by `track_edges`, so a curved one along the curve,
    or, where OSM maps no track beside it, straight, along its outline's longest side.
    A platform OSM splits into pieces is measured whole.

    Each of `platforms.csv`'s stops is at the edge beside the track
    its route's OSM relation stops on there, going the same way,
    by the relation's stop on that track:
    the most trains' where a stop's trains stop at both edges of an island,
    as locals and expresses at an island between them,
    or the platform's longest edge where no relation's stop is on either.

    The extract is read twice, for the ways' nodes and then their locations,
    not with every node's location at hand, which takes over a gigabyte.
    """
    # `lidar` reads this module's table.
    from mta_od_data.lidar import PlatformAxis, ground_outline

    rows = [r for r in _rows(platforms) if r["platform"].startswith("w")]
    coords = {
        s["gtfs_stop_id"]: (float(s["gtfs_longitude"]), float(s["gtfs_latitude"]))
        for s in _rows(stations)
    }
    outlined = _PlatformWays()
    outlined.apply_file(str(extract))
    pieces = {
        w: outlined.pieces(w)
        for w in {r["platform"] for r in rows}
        if w in outlined.nodes
    }
    # Each route's stops at each platform, by the relations:
    # its stop on the track, and the stops before and after it.
    stops_at: dict[tuple[str, str], list[_RelationStop]] = defaultdict(list)
    for route, members in outlined.relations:
        listed = _relation_stops(members)
        for i, (node, platform) in enumerate(listed):
            stops_at[route, platform].append(
                _RelationStop(
                    node,
                    listed[i - 1][0] if i > 0 else node,
                    listed[i + 1][0] if i + 1 < len(listed) else node,
                )
            )
    locations = _NodeLocations(
        {n for ps in pieces.values() for p in ps for n in outlined.nodes[p]}
        | set(outlined.joined)
        | {
            n
            for ss in stops_at.values()
            for s in ss
            for n in (s.node, s.before, s.after)
        }
    )
    locations.apply_file(str(extract))
    track_nodes = [n for n in outlined.joined if n in locations.at]
    track_at = np.array([locations.at[n] for n in track_nodes]).reshape(-1, 2)

    def outline(way: str) -> list[tuple[float, float]] | None:
        nodes = outlined.nodes[way]
        at = [locations.at[n] for n in nodes if n in locations.at]
        # Outlined, not mapped as a line or with nodes missing.
        return at if len(at) == len(nodes) > 3 and nodes[0] == nodes[-1] else None

    def tracks(origin: tuple[float, float]) -> Tracks:
        """The tracks within about 600 m of `origin`, in metres from it,
        as `ground_outline` puts a platform."""
        near = np.flatnonzero(
            (np.abs(track_at[:, 0] - origin[0]) < 0.008)
            & (np.abs(track_at[:, 1] - origin[1]) < 0.006)
        )
        xy = _metres(track_at[near], origin)
        return Tracks(
            {
                track_nodes[i]: (float(x), float(y))
                for i, (x, y) in zip(near, xy, strict=True)
            },
            outlined.joined,
        )

    # Each platform's edges, and where it's measured from.
    measured: dict[str, tuple[list[TrackEdge], tuple[float, float]]] = {}
    for way, ps in pieces.items():
        outlines = [o for p in sorted(ps) if (o := outline(p))]
        if outline(way) and outlines:
            origin = outlines[0][0]
            whole = unary_union([ground_outline(o, origin) for o in outlines])
            # Or straight, along the longest side of its pieces' hull.
            edges = track_edges(whole, tracks(origin)) or [
                TrackEdge(PlatformAxis.of(whole.convex_hull).length, LineString())
            ]
            measured[way] = (edges, origin)

    def edge(r: dict[str, str]) -> int | None:
        """Which of its platform's edges the stop `r` of `platforms.csv` is at."""
        edges, origin = measured[r["platform"]]
        here = coords.get(r["stop"])
        before = coords.get(r["prev_stop"], here)
        after = coords.get(r["next_stop"], here)
        if len(edges) == 1 or here is None or before is None or after is None:
            return 0
        going = _metres(np.array([after]), before)[0]
        for s in stops_at.get((r["route"], r["platform"]), []):
            if not {s.node, s.before, s.after} <= locations.at.keys():
                continue
            travel = _metres(np.array([locations.at[s.after]]), locations.at[s.before])[
                0
            ]
            if travel @ going <= 0:
                continue
            node = Point(_metres(np.array([locations.at[s.node]]), origin)[0])
            apart, i = min((e.track.distance(node), i) for i, e in enumerate(edges))
            # On its track, not another.
            if apart < 1:
                return i
        return None

    trains: dict[tuple[str, str], Counter[int]] = defaultdict(Counter)
    for r in rows:
        if r["platform"] in measured and (i := edge(r)) is not None:
            trains[r["stop"] + r["direction"], r["platform"]][i] += int(r["trains"])
    feet: dict[tuple[str, str], float] = {}
    longest: dict[str, tuple[float, str]] = {}
    for r in rows:
        if r["platform"] not in measured:
            continue
        edges, _ = measured[r["platform"]]
        key = (r["stop"] + r["direction"], r["platform"])
        most = trains[key].most_common(1)
        ft = max(e.metres for e in edges) / 0.3048
        feet[key] = edges[most[0][0]].metres / 0.3048 if most else ft
        longest[r["stop"]] = max(longest.get(r["stop"], (0.0, "")), (ft, r["platform"]))
    return OsmLengths(longest, feet)


@dataclass(frozen=True, slots=True)
class _RelationStop:
    """A route relation's stop at a platform, a node on its track,
    and its stops before and after, or itself where it has none."""

    node: int
    before: int
    after: int


def _relation_stops(members: list[tuple[str, int, str]]) -> list[tuple[int, str]]:
    """A route relation's stops on the tracks, each with the platform after it,
    as `platforms.fetch_platforms` pairs them."""
    out = []
    stop = None
    for kind, ref, role in members:
        if role.startswith("stop"):
            stop = ref if kind == "n" else None
        elif role.startswith("platform") and stop is not None:
            out.append((stop, f"{kind}{ref}"))
            stop = None
    return out


def _metres(points: np.ndarray, origin: tuple[float, float]) -> np.ndarray:
    """`(lon, lat)` points in metres east and north of `origin`,
    as `ground_outline` puts a platform."""
    lon0, lat0 = origin
    return np.stack(
        [
            (points[:, 0] - lon0) * 111_320 * cos(radians(lat0)),
            (points[:, 1] - lat0) * 110_540,
        ],
        1,
    )


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
            return SIR_FT, "SIR train"
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
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Every entrance's time between the street and its station's platforms,
    without the walk along them,
    and the length of the edge of each platform each stop's trains stop at,
    by direction."""
    entrances = _rows(_download(ENTRANCES_URL, DIR / "entrances.csv"))
    lifts = lift_depths(_rows(_download(LIFTS_URL, DIR / "lifts.csv")))
    osm = json.loads(
        _download(
            OVERPASS_URL, DIR / "platforms.json", {"data": OVERPASS_QUERY}
        ).read_text()
    )
    by_id = depths(_rows(stations_csv), lifts, osm)
    lengths = osm_lengths(extract, stations=stations_csv)

    def row(gtfs_id: str, lat: float, lon: float, kind: str) -> dict[str, object]:
        depth = by_id[gtfs_id]
        complex_id = depth.station["complex_id"]
        walk = WALKS.get((lat, lon))
        along = 0.0 if walk else platform_ft(depth.station, lat, lon)
        # Blank for a long walk inside the station, timed to the platform's middle.
        length = None if walk else platform_length(depth.station, lengths.longest)
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
    edges: list[dict[str, object]] = [
        {"stop": stop, "platform": way, "length_ft": round(ft)}
        for (stop, way), ft in sorted(lengths.edges.items())
    ]
    return rows, edges


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
def fetch_station_access() -> None:
    """
    Rebuild each station entrance's time to the platforms, `data/station_access.csv`,
    and each stop's platform edge's length, `data/platform_edges.csv`,
    from the MTA's and OSM's data now, to review and commit.
    """
    rows, edges = build(fetch_stations(), fetch_extract())
    TABLE.parent.mkdir(parents=True, exist_ok=True)
    for path, columns, table in [(TABLE, COLUMNS, rows), (EDGES, EDGE_COLUMNS, edges)]:
        with path.open("w", newline="") as f:
            out = DictWriter(f, columns, lineterminator="\n")
            out.writeheader()
            out.writerows(table)
    print(
        f"{len(rows)} entrances of {len({r['station'] for r in rows})} stations,"
        f" and {len(edges)} stops' platform edges"
    )
