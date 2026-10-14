"""Which physical platform each route's trains stop at,
from OpenStreetMap's NYC Subway route relations
(© OpenStreetMap contributors, under the ODbL: https://www.openstreetmap.org/copyright).

GTFS has each station's directions (`127N`, `127S`), not its platforms:
an island platform serves both directions, and an express station has two platforms
a direction.
OSM maps each platform, and each route's relation (one a direction and service pattern,
in the PTv2 scheme) lists its stops in order, each followed by its platform.
Each relation's stops are matched to the nearest GTFS stop its route serves,
so each pair of consecutive stops a route makes maps to the platforms it stops at:
which also tells express from local platforms of the same route and direction.

Where a feed's route and OSM's relations disagree on its stops
(a station closed, or a reroute OSM doesn't have),
a stop's platform falls back to its route's at that stop in that direction,
then to the stop's in that direction if one platform serves it.

Each platform's area is its OSM outline's, for how crowded it is (`platform_areas.csv`):
every platform a route relation lists is mapped as a closed way
but one, Elmhurst Av's northbound, a multipolygon relation, left without.

Read from Geofabrik's New York extract, not the Overpass API,
whose public servers were too busy to answer.
"""

import csv
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import pairwise
from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve
from zipfile import ZipFile

import osmium
from osmium.osm import Node, Relation, Way
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.gtfs import DEFAULT_GTFS_DIR
from mta_od_data.ridership.service import load_feed

app = Typer()

EXTRACT_URL = "https://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf"
DEFAULT_EXTRACT = DATA / "osm" / "new-york-latest.osm.pbf"
DEFAULT_OUT = Path(__file__).parent / "ridership" / "platforms.csv"
DEFAULT_AREAS_OUT = Path(__file__).parent / "ridership" / "platform_areas.csv"

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


def metres(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Roughly, at New York's latitude: plenty to tell stations apart."""
    return math.hypot((a[0] - b[0]) * 111_000, (a[1] - b[1]) * 84_000)


def square_metres(ring: list[tuple[float, float]]) -> float:
    """A closed ring's area, by the shoelace formula,
    on a plane through its first point: exact enough across a platform."""
    lat0 = math.radians(ring[0][0])
    xy = [(lon * 111_320 * math.cos(lat0), lat * 111_320) for lat, lon in ring]
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in pairwise(xy))) / 2


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

    # (route, stop, next stop) -> (stop's platform, next stop's), over every feed.
    pairs: dict[tuple[str, str, str], tuple[str, str]] = {}
    # (route, stop, direction) and (stop, direction) -> platform -> times seen.
    by_route_dir: defaultdict[tuple[str, str, str], Counter[str]] = defaultdict(Counter)
    by_dir: defaultdict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    directions: dict[tuple[str, str, str], tuple[str, str]] = {}
    for feed_zip in sorted(gtfs_dir.glob("*.zip")):
        feed = load_feed(feed_zip)
        directions |= feed.directions
        coords = stop_coords(feed_zip)
        served: defaultdict[str, set[str]] = defaultdict(set)
        for p in feed.patterns:
            served[p.route].update(s for s in p.stops if s in coords)
        for route, ms in relations.relations:
            # Each matched stop, and its platform: the platform member after it.
            stops: list[tuple[str, str]] = []
            stop = None
            for t, ref, role in ms:
                key = f"{t[0]}{ref}"
                if role.startswith("stop") and key in locations.at and served[route]:
                    at = locations.at[key]
                    d, s = min((metres(at, coords[s]), s) for s in served[route])
                    stop = s if d <= MAX_MATCH_METRES else None
                elif role.startswith("platform") and stop is not None:
                    stops.append((stop, key))
                    stop = None
            for (a, pa), (b, pb) in zip(stops, stops[1:], strict=False):
                pairs.setdefault((route, a, b), (pa, pb))
                if (route, a, b) in feed.directions:
                    da, db = feed.directions[route, a, b]
                    by_route_dir[route, a, da][pa] += 1
                    by_route_dir[route, b, db][pb] += 1
                    by_dir[a, da][pa] += 1
                    by_dir[b, db][pb] += 1

    def platform(route: str, stop: str, direction: str) -> str:
        """A stop's platform when its pair isn't in any relation."""
        if seen := by_route_dir.get((route, stop, direction)):
            return seen.most_common(1)[0][0]
        if seen := by_dir.get((stop, direction)):
            return seen.most_common(1)[0][0]
        return ""

    rows = []
    for (route, a, b), (da, db) in sorted(directions.items()):
        pa, pb = pairs.get((route, a, b), ("", ""))
        rows.append(
            (
                route,
                a,
                b,
                da,
                pa or platform(route, a, da),
                pb or platform(route, b, db),
            )
        )
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "route",
                "stop",
                "next_stop",
                "direction",
                "stop_platform",
                "next_platform",
            ]
        )
        writer.writerows(rows)
    direct = sum((r[0], r[1], r[2]) in pairs for r in rows)
    unknown = sum(not r[4] or not r[5] for r in rows)
    print(
        f"wrote {out}: {len(rows)} pairs of stops, {direct} from a relation directly, "
        f"{unknown} with a platform unknown"
    )
    platforms = sorted({p for r in rows for p in (r[4], r[5]) if p})
    with areas_out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["platform", "area_m2"])
        writer.writerows(
            (p, f"{locations.areas[p]:.1f}") for p in platforms if p in locations.areas
        )
    missing = [p for p in platforms if p not in locations.areas]
    print(
        f"wrote {areas_out}: {len(platforms) - len(missing)} platforms' areas, "
        f"{len(missing)} not closed ways: {', '.join(missing)}"
    )
