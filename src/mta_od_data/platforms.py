"""Which physical platform each route's trains stop at,
from OpenStreetMap's NYC Subway route relations
(© OpenStreetMap contributors, under the ODbL: https://www.openstreetmap.org/copyright).

GTFS has each station's directions (`127N`, `127S`), not its platforms:
an island platform serves both directions, and an express station has two platforms
a direction.
OSM maps each platform, and each route's relation (one a direction and service pattern,
in the PTv2 scheme) lists its stops in order, each followed by its platform.
Each relation's stops are matched to the nearest GTFS stop its route serves,
so each stop a route makes, with the stops before and after it,
maps to the platform it stops at:
which also tells express from local platforms of the same route and direction,
and a route's trains that stop at different platforms by how they run,
like the 2 uptown at 34 St-Penn Station, express by day and local late at night.
Where relations differ, the one the feeds have more trains like wins.

Where a feed's route and OSM's relations disagree on its stops
(a station closed, or a reroute OSM doesn't have),
a stop's platform falls back to its route's there with the same next stop,
then the same previous stop, then its route's at that stop in that direction,
then to the stop's in that direction if one platform serves it.

Each platform's area is its OSM outline's, for how crowded it is (`platform_areas.csv`):
every platform a route relation lists is mapped as a closed way
but one, Elmhurst Av's northbound, a multipolygon relation, left without.
A few are mapped in pieces, which a relation lists one after another after its stop,
like Newkirk Plaza's southbound, in four:
such a platform is its first piece, with all its pieces' area.

Platforms stacked one right over another, on different levels (by OSM's `level`)
and overlapping by at least half the smaller one,
are a flight of stairs a level apart, for OSM transfers (`stacked_platforms.csv`):
7 Av's on 53 St, say, one level apart, or W 4 St's, two,
but not 59 St-Columbus Circle's 1 and A/B/C/D, crossing at an angle,
nor 74 St-Broadway's 7, on the el.

Read from Geofabrik's New York extract, not the Overpass API,
whose public servers were too busy to answer.
"""

import csv
import math
from collections import Counter, defaultdict
from contextlib import suppress
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve
from zipfile import ZipFile

import osmium
from osmium.osm import Node, Relation, Way
from shapely import STRtree, union_all
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.gtfs import DEFAULT_GTFS_DIR
from mta_od_data.ridership.service import Feed, load_feed

app = Typer()

EXTRACT_URL = "https://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf"
DEFAULT_EXTRACT = DATA / "osm" / "new-york-latest.osm.pbf"
DEFAULT_OUT = Path(__file__).parent / "ridership" / "platforms.csv"
DEFAULT_AREAS_OUT = Path(__file__).parent / "ridership" / "platform_areas.csv"
# Beside `platforms.csv`, where RAPTOR looks for it.
DEFAULT_STACKED_OUT = Path(__file__).parent / "ridership" / "stacked_platforms.csv"

# Two platforms on different levels overlapping by at least this much of the smaller
# are stacked: on OSM's, those a level apart overlap 68% or more, or 28% or less.
STACKED_OVERLAP = 0.5

# A relation's stop more than this far from every GTFS stop of its route
# is one the feed doesn't have (or a mapping error), and is skipped.
MAX_MATCH_METRES = 300

# Shuttles are all `S` in OSM; GTFS has a route each.
SHUTTLES = {"42nd": "GS", "Franklin": "FS", "Rockaway": "H"}


@dataclass(frozen=True, slots=True)
class Member:
    role: str
    lat: float
    lon: float
    # The platform's OSM element, e.g. `w426103243`.
    id: str


class Relations(osmium.SimpleHandler):
    """NYC Subway route relations: each one's route and members, in order."""

    def __init__(self) -> None:
        super().__init__()
        self.relations: list[tuple[str, list[tuple[str, int, str]]]] = []

    def relation(self, r: Relation) -> None:
        tags = r.tags
        if tags.get("route") != "subway" or tags.get("network") != "NYC Subway":
            return
        ref, name = tags.get("ref") or "", tags.get("name") or ""
        if ref.startswith("<"):
            route = ref.strip("<>") + "X"
        elif ref == "S":
            route = next((v for k, v in SHUTTLES.items() if k in name), "")
        else:
            route = ref
        members = [(m.type, m.ref, m.role) for m in r.members if m.role]
        self.relations.append((route, members))


class Locations(osmium.SimpleHandler):
    """Each wanted node's location, and each wanted way's centroid,
    and its area if it's closed."""

    def __init__(self, nodes: set[int], ways: set[int]) -> None:
        super().__init__()
        self.wanted_nodes, self.wanted_ways = nodes, ways
        self.at: dict[str, tuple[float, float]] = {}
        self.areas: dict[str, float] = {}
        # Each closed way's outline, in `(lat, lon)`, and its `level`, if a number.
        self.rings: dict[str, list[tuple[float, float]]] = {}
        self.levels: dict[str, float] = {}

    def node(self, n: Node) -> None:
        if n.id in self.wanted_nodes:
            self.at[f"n{n.id}"] = (n.location.lat, n.location.lon)

    def way(self, w: Way) -> None:
        if w.id in self.wanted_ways:
            points = [(nd.lat, nd.lon) for nd in w.nodes if nd.location.valid()]
            if points:
                self.at[f"w{w.id}"] = (
                    sum(p[0] for p in points) / len(points),
                    sum(p[1] for p in points) / len(points),
                )
            if w.is_closed() and len(points) == len(w.nodes) > 3:
                self.areas[f"w{w.id}"] = square_metres(points)
                self.rings[f"w{w.id}"] = points
            with suppress(ValueError):
                self.levels[f"w{w.id}"] = float(w.tags.get("level") or "")


def metres(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Roughly, at New York's latitude: plenty to tell stations apart."""
    return math.hypot((a[0] - b[0]) * 111_000, (a[1] - b[1]) * 84_000)


def square_metres(ring: list[tuple[float, float]]) -> float:
    """A closed ring's area, by the shoelace formula,
    on a plane through its first point: exact enough across a platform."""
    lat0 = math.radians(ring[0][0])
    xy = [(lon * 111_320 * math.cos(lat0), lat * 111_320) for lat, lon in ring]
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in pairwise(xy))) / 2


def plane(ring: list[tuple[float, float]]) -> BaseGeometry:
    """A ring as a polygon in metres, on a plane through New York."""
    k = 111_320 * math.cos(math.radians(40.7))
    return Polygon([(lon * k, lat * 111_320) for lat, lon in ring]).buffer(0)


def stacked(
    platforms: list[str], pieces: dict[str, set[str]], locations: Locations
) -> list[tuple[str, str, int, float]]:
    """Each pair of `platforms` stacked one over another,
    how many levels apart, and how much they overlap."""
    shapes: dict[str, BaseGeometry] = {}
    for p in platforms:
        parts = pieces.get(p) or {p}
        if p in locations.levels and all(q in locations.rings for q in parts):
            shapes[p] = union_all([plane(locations.rings[q]) for q in parts])
    names = sorted(shapes)
    tree = STRtree([shapes[p] for p in names])
    pairs = []
    for i, j in zip(*tree.query([shapes[p] for p in names], "intersects"), strict=True):
        a, b = names[i], names[j]
        levels = abs(locations.levels[a] - locations.levels[b])
        if a >= b or levels < 1:
            continue
        overlap = shapes[a].intersection(shapes[b]).area / min(
            shapes[a].area, shapes[b].area
        )
        if overlap >= STACKED_OVERLAP:
            pairs.append((a, b, round(levels), overlap))
    return pairs


def direction(feed: Feed, route: str, prev: str, stop: str, next_: str) -> str | None:
    """The direction `route`'s trains stopping at `stop` between those go there."""
    if (d := feed.directions.get((route, stop, next_))) is not None:
        return d[0]
    if (d := feed.directions.get((route, prev, stop))) is not None:
        return d[1]
    return None


def stop_coords(feed_zip: Path) -> dict[str, tuple[float, float]]:
    """Each GTFS parent stop's location."""
    from io import TextIOWrapper

    with ZipFile(feed_zip) as z, z.open("stops.txt") as f:
        return {
            r["stop_id"]: (float(r["stop_lat"]), float(r["stop_lon"]))
            for r in csv.DictReader(TextIOWrapper(f, "utf-8-sig"))
            if not r["parent_station"]
        }


@app.command()
def fetch_platforms(
    extract: Annotated[
        Path, Option(help="Geofabrik's New York OSM extract, fetched if missing")
    ] = DEFAULT_EXTRACT,
    gtfs_dir: Annotated[
        Path, Option(help="Feed versions, from `mta-od-data fetch-gtfs`")
    ] = DEFAULT_GTFS_DIR,
    out: Annotated[
        Path, Option(help="The platform of each route's stops")
    ] = DEFAULT_OUT,
    areas_out: Annotated[
        Path, Option(help="Each of those platforms' area")
    ] = DEFAULT_AREAS_OUT,
    stacked_out: Annotated[
        Path, Option(help="Those platforms stacked one right over another")
    ] = DEFAULT_STACKED_OUT,
) -> None:
    """Map each route's consecutive stops, in every feed version,
    to the OSM platforms its trains stop at there."""
    if not extract.exists():
        extract.parent.mkdir(parents=True, exist_ok=True)
        print(f"fetching {EXTRACT_URL}")
        urlretrieve(EXTRACT_URL, extract)
    relations = Relations()
    relations.apply_file(str(extract))
    members = [m for _, ms in relations.relations for m in ms]
    locations = Locations(
        {ref for t, ref, _ in members if t == "n"},
        {ref for t, ref, _ in members if t == "w"},
    )
    locations.apply_file(str(extract), locations=True)
    print(f"{len(relations.relations)} route relations")

    # (route, previous stop, stop, next stop) -> platform -> trains, over every feed,
    # "" for no previous or next stop.
    exact: defaultdict[tuple[str, str, str, str], Counter[str]] = defaultdict(Counter)
    # The same without the previous stop, and without the next.
    by_next: defaultdict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    by_previous: defaultdict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    # (route, stop, direction) and (stop, direction) -> platform -> trains.
    by_route_dir: defaultdict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    by_dir: defaultdict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    # Each platform's pieces, by its first: itself, and those listed right after it.
    pieces: defaultdict[str, set[str]] = defaultdict(set)
    # The feeds' trains stopping at each (route, previous stop, stop, next stop),
    # and each one's direction there.
    trains: Counter[tuple[str, str, str, str]] = Counter()
    directions: dict[tuple[str, str, str, str], str] = {}
    for feed_zip in sorted(gtfs_dir.glob("*.zip")):
        feed = load_feed(feed_zip)
        coords = stop_coords(feed_zip)
        served: defaultdict[str, set[str]] = defaultdict(set)
        # This feed's trains stopping at each (route, previous stop, stop, next stop).
        feed_trains: Counter[tuple[str, str, str, str]] = Counter()

        for p, n in feed.patterns.items():
            served[p.route].update(s for s in p.stops if s in coords)
            padded = ("", *p.stops, "")
            for key in zip(padded, padded[1:], padded[2:], strict=False):
                feed_trains[p.route, *key] += n
                if (d := direction(feed, p.route, *key)) is not None:
                    directions[p.route, *key] = d
        trains += feed_trains

        for route, ms in relations.relations:
            # Each matched stop, and its platform: the platform member after it.
            stops: list[tuple[str, str]] = []
            stop = None
            # The platform being listed, so its further pieces are its.
            first = None
            for t, ref, role in ms:
                key = f"{t[0]}{ref}"
                if not role.startswith("platform"):
                    first = None
                if role.startswith("stop") and key in locations.at and served[route]:
                    # A stop listed without its platform, as 66 St on the uptown 1,
                    # still counts as the stop before and after its neighbours.
                    if stop is not None:
                        stops.append((stop, ""))
                    at = locations.at[key]
                    d, s = min((metres(at, coords[s]), s) for s in served[route])
                    stop = s if d <= MAX_MATCH_METRES else None
                elif role.startswith("platform") and first is not None:
                    pieces[first].add(key)
                elif role.startswith("platform") and stop is not None:
                    stops.append((stop, key))
                    stop, first = None, key
                    pieces[key].add(key)
            if stop is not None:
                stops.append((stop, ""))
            padded = [("", ""), *stops, ("", "")]
            for (prev, _), (stop, platform), (next_, _) in zip(
                padded, padded[1:], padded[2:], strict=False
            ):
                if not platform:
                    continue
                key = (route, prev, stop, next_)
                # The feed's trains stopping as the relation does there,
                # so where two relations of a route differ, as the 2 express by day
                # and local by night, uptown at Penn, the busier one's platform wins.
                # At least 1, so a relation the feed has no trains like still counts.
                n = max(1, feed_trains[key])
                exact[key][platform] += n
                by_next[route, stop, next_][platform] += n
                by_previous[route, prev, stop][platform] += n
                # From the stop before or after alone,
                # as a relation may skip a stop the feed has.
                if (d := direction(feed, *key)) is not None:
                    by_route_dir[route, stop, d][platform] += n
                    by_dir[stop, d][platform] += n

    def platform(route: str, prev: str, stop: str, next_: str, d: str) -> str:
        """The platform trains stop at, from the relations stopping most like them."""
        for seen in (
            exact.get((route, prev, stop, next_)),
            by_next.get((route, stop, next_)) if next_ else None,
            by_previous.get((route, prev, stop)) if prev else None,
            by_route_dir.get((route, stop, d)),
            by_dir.get((stop, d)),
        ):
            if seen:
                return seen.most_common(1)[0][0]
        return ""

    rows = sorted(
        (*key, d, platform(*key, d), n)
        for key, n in trains.items()
        if (d := directions.get(key)) is not None
    )
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "route",
                "prev_stop",
                "stop",
                "next_stop",
                "direction",
                "platform",
                "trains",
            ]
        )
        writer.writerows(rows)
    direct = sum(r[:4] in exact for r in rows)
    unknown = sum(not r[5] for r in rows)
    print(
        f"wrote {out}: {len(rows)} stops with the stops before and after, "
        f"{direct} from a relation directly, {unknown} with a platform unknown"
    )
    platforms = sorted({r[5] for r in rows if r[5]})

    def area(p: str) -> float | None:
        parts = pieces.get(p) or {p}
        if not all(q in locations.areas for q in parts):
            return None
        return sum(locations.areas[q] for q in parts)

    areas = {p: a for p in platforms if (a := area(p)) is not None}
    with areas_out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["platform", "area_m2"])
        writer.writerows((p, f"{a:.1f}") for p, a in areas.items())
    missing = [p for p in platforms if p not in areas]
    print(
        f"wrote {areas_out}: {len(platforms) - len(missing)} platforms' areas, "
        f"{len(missing)} not closed ways: {', '.join(missing)}"
    )

    pairs = stacked(platforms, pieces, locations)
    with stacked_out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["platform", "other", "levels", "overlap"])
        writer.writerows((a, b, n, f"{o:.2f}") for a, b, n, o in pairs)
    print(f"wrote {stacked_out}: {len(pairs)} pairs of platforms stacked")
