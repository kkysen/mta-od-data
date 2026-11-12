"""Walks between a station's platforms along OSM's indoor ways
(© OpenStreetMap contributors, under the ODbL: https://www.openstreetmap.org/copyright),
for `raptor`'s transfers where no LiDAR map covers a station (`raptor/osm_walks.csv`),
once checked against LiDAR walks and riders' knowledge: `raptor` doesn't read them yet.

OSM maps many stations' insides: footways and corridors on each level,
`highway=steps` between levels (`level=-2;-1`), escalators as steps with `conveying`,
and elevators, which are left out, as riders who can take stairs do.
Platforms and indoor areas (`indoor=area` or `corridor`)
are walked across in straight lines
between their outlines' nodes and the ways' ends OSM draws in or by them.
A walk is the quickest path over them
from any node on one platform's level, on or in it,
to any on or in another's, timed at `raptor`'s default speeds
to pick it, the same as LiDAR walks (`lidar.Walk`).

It stays inside the fare gates: never through a turnstile, gate, or entrance node.
A flight climbs as many levels as its `level` spans, each `lidar.DEFAULT_RISE`,
its run its length on the map;
which end is up is from its `incline`, or else the levels of the ways at each end,
and each end joins only what's on its own level,
so a flight drawn wholly inside a platform still climbs from it.
An escalator runs the way its `conveying` says; where that's only `yes`,
a lone one between two levels nearby runs up, and of two or more,
either way, as one runs each way.
"""

import csv
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import pairwise
from math import cos, hypot, radians
from pathlib import Path
from typing import Annotated

import numpy as np
import osmium
from osmium.osm import Node, Way
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from shapely import STRtree, contains_xy
from shapely.geometry import Point, Polygon
from typer import Option, Typer

from mta_od_data.lidar import DEFAULT_RISE, Walk
from mta_od_data.platforms import DEFAULT_AREAS_OUT, DEFAULT_EXTRACT

app = Typer()

DEFAULT_OUT = Path(__file__).parents[2] / "raptor" / "osm_walks.csv"

# How far from a platform OSM's ways are read, in metres.
NEAR_M = 400
# Platforms farther apart than this aren't one station's.
PAIR_M = 400
# The longest walk kept, in metres on the level.
MAX_WALK_M = 600
# How near an escalator runs another between the same levels to be its pair.
ESCALATOR_PAIR_M = 30
# Nodes a walk never passes, leaving the fare-controlled area.
BARRIERS = {"turnstile", "full-height_turnstile", "gate", "swing_gate", "lift_gate"}
WALKED = {"footway", "corridor", "pedestrian", "path", "steps", "platform"}
# How near an area a flight's end or a footway on its level is, to join it.
SNAP_M = 3.0
# Indoor areas walked across: a mezzanine's floor, a passage.
AREAS = {"area", "corridor"}
K_LON = 111_320 * cos(radians(40.7))
K_LAT = 111_320


def xy(lon: float, lat: float) -> tuple[float, float]:
    return lon * K_LON, lat * K_LAT


def levels(tag: str | None) -> list[float]:
    out = []
    for part in (tag or "").split(";"):
        try:
            out.append(float(part))
        except ValueError:
            continue
    return out


class Platforms(osmium.SimpleHandler):
    def __init__(self, wanted: set[int]) -> None:
        super().__init__()
        self.wanted = wanted
        self.outlines: dict[str, Polygon] = {}
        self.levels: dict[str, list[float]] = {}

    def way(self, w: Way) -> None:
        if w.id not in self.wanted or not w.is_closed():
            return
        try:
            ring = [xy(n.lon, n.lat) for n in w.nodes]
        except osmium.InvalidLocationError:
            return
        if len(ring) > 3:
            self.outlines[f"w{w.id}"] = Polygon(ring).buffer(0)
            self.levels[f"w{w.id}"] = levels(w.tags.get("level"))


@dataclass
class Ways(osmium.SimpleHandler):
    near: STRtree
    ways: list[tuple[int, dict[str, str], list[int]]] = field(default_factory=list)
    at: dict[int, tuple[float, float]] = field(default_factory=dict)
    blocked: set[int] = field(default_factory=set)

    def __post_init__(self) -> None:
        super().__init__()

    def node(self, n: Node) -> None:
        t = n.tags
        if (
            t.get("barrier") in BARRIERS
            or "entrance" in t
            or t.get("railway") == "subway_entrance"
            or t.get("highway") == "elevator"
        ):
            self.blocked.add(n.id)

    def way(self, w: Way) -> None:
        t = dict(w.tags)
        hw = t.get("highway")
        if (hw not in WALKED and not is_area(t)) or t.get("access") in (
            "no",
            "private",
        ):
            return
        try:
            pts = [(n.ref, xy(n.lon, n.lat)) for n in w.nodes]
        except osmium.InvalidLocationError:
            return
        mid = pts[len(pts) // 2][1]
        if not len(self.near.query(Polygon.from_bounds(*mid, *mid).buffer(NEAR_M))):
            return
        for ref, p in pts:
            self.at[ref] = p
        self.ways.append((w.id, dict(t), [ref for ref, _ in pts]))


@dataclass(frozen=True, slots=True)
class Edge:
    a: int
    b: int
    metres: float
    # Levels climbed going from `a` to `b`, or `None` if on the level;
    # `nan` where which end is up is unknown.
    climb: float | None = None
    escalator: bool = False
    # Whether it can be walked from `b` to `a` too.
    both: bool = True


def is_area(t: dict[str, str]) -> bool:
    """An area walked across in any straight line: a platform, or an indoor floor."""
    return (
        t.get("railway") == "platform"
        or t.get("public_transport") == "platform"
        or t.get("indoor") in AREAS
        or t.get("area") == "yes"
        and t.get("highway") in WALKED
    )


def edges(ways: Ways) -> tuple[list[Edge], dict[int, float]]:
    """Every way's edges, and edges across each area,
    between any two nodes on its outline or attached to it:
    the end of a flight on its level, or a footway on its level, within `SNAP_M`,
    as OSM often draws them inside a platform without sharing a node.
    An area's outline nodes are copies on its level, joined to the node itself
    only where a way on that level runs through it,
    as a platform and the mezzanine over it may share a node.
    Returns the edges, and the level of each node on one."""
    areas = [
        (t, nodes[:-1], Polygon([ways.at[n] for n in nodes]).buffer(0))
        for _, t, nodes in ways.ways
        if is_area(t) and nodes[0] == nodes[-1] and len(nodes) > 3
    ]
    tree = STRtree([poly for _, _, poly in areas])

    def within(n: int, level: float) -> list[int]:
        """The areas on `level` node `n` is in or by."""
        pt = Point(ways.at[n])
        return [
            i
            for i in tree.query(pt.buffer(SNAP_M))
            if levels(areas[i][0].get("level")) == [level]
            and areas[i][2].distance(pt) <= SNAP_M
        ]

    node_levels: dict[int, set[float]] = defaultdict(set)
    for _, t, nodes in ways.ways:
        lv = levels(t.get("level"))
        if t.get("highway") != "steps" and not is_area(t) and len(lv) == 1:
            for n in nodes:
                node_levels[n].add(lv[0])
    attached: dict[int, set[int]] = defaultdict(set)
    level_of = {n: next(iter(lv)) for n, lv in node_levels.items() if len(lv) == 1}
    copies: dict[tuple[int, float], int] = {}
    out = []

    def copy(n: int, level: float) -> int:
        if (n, level) not in copies:
            c = copies[(n, level)] = -(10**13) - len(copies)
            ways.at[c] = ways.at[n]
            level_of[c] = level
            if level in node_levels[n]:
                out.append(Edge(c, n, 0.0))
        return copies[(n, level)]

    escalators = [
        (t, nodes)
        for _, t, nodes in ways.ways
        if t.get("highway") == "steps" and t.get("conveying") not in (None, "no")
    ]
    for wid, t, nodes in ways.ways:
        if is_area(t) and nodes[0] == nodes[-1]:
            continue
        pts = [ways.at[n] for n in nodes]
        lengths = [hypot(p[0] - q[0], p[1] - q[1]) for p, q in pairwise(pts)]
        lv = levels(t.get("level"))
        # A footway between levels is a ramp or a flight drawn as one, climbed as steps.
        if t.get("highway") != "steps" and len(lv) < 2:
            out.extend(
                Edge(a, b, m)
                for (a, b), m in zip(pairwise(nodes), lengths, strict=True)
            )
            if len(lv) == 1:
                for n in nodes:
                    for i in within(n, lv[0]):
                        attached[i].add(n)
            continue
        if len(lv) < 2:
            # Steps on one level, or none given: walked as a footway.
            out.extend(
                Edge(a, b, m)
                for (a, b), m in zip(pairwise(nodes), lengths, strict=True)
            )
            continue
        low, high = min(lv), max(lv)
        # Up from its first node to its last, or down, or unknown.
        sign = {"up": 1.0, "down": -1.0}.get(t.get("incline", ""), 0.0)
        if not sign:
            first, last = node_levels[nodes[0]], node_levels[nodes[-1]]
            if low in first or high in last:
                sign = 1.0
            elif high in first or low in last:
                sign = -1.0
        # Its bottom and top, apart from its end nodes, which OSM often draws
        # both inside the platform below and the floor above:
        # each joins the ways and areas on its own level by its end.
        ends = (nodes[0], nodes[-1]) if sign >= 0 else (nodes[-1], nodes[0])
        bottom, top = -2 * wid, -2 * wid - 1
        ways.at[bottom], ways.at[top] = ways.at[ends[0]], ways.at[ends[1]]
        level_of[bottom], level_of[top] = low, high
        for virtual, end, level in ((bottom, ends[0], low), (top, ends[1], high)):
            if level in node_levels[end] or (sign and not node_levels[end]):
                out.append(Edge(virtual, end, 0.0))
            for i in within(end, level):
                attached[i].add(virtual)
        total = sum(lengths) or 1.0
        span = high - low
        conveying = t.get("conveying")
        escalator = conveying not in (None, "no")
        if escalator and sign and conveying in ("forward", "backward"):
            up = (conveying == "forward") == (sign > 0)
            a, b = (bottom, top) if up else (top, bottom)
            out.append(Edge(a, b, total, span if up else -span, True, both=False))
            continue
        if escalator:
            mid = pts[len(pts) // 2]
            paired = sum(
                hypot(
                    ways.at[n2[len(n2) // 2]][0] - mid[0],
                    ways.at[n2[len(n2) // 2]][1] - mid[1],
                )
                < ESCALATOR_PAIR_M
                for t2, n2 in escalators
                if t2.get("level") == t.get("level")
            )
            if paired < 2:
                # A lone escalator runs up.
                out.append(Edge(bottom, top, total, span, True, both=False))
                continue
        out.append(Edge(bottom, top, total, span, escalator))
    for i, (t, ring, _) in enumerate(areas):
        lv = levels(t.get("level"))
        ring = [copy(n, lv[0]) for n in ring] if len(lv) == 1 else ring
        across = list(dict.fromkeys([*ring, *attached[i]]))
        out.extend(
            Edge(
                a,
                b,
                hypot(ways.at[a][0] - ways.at[b][0], ways.at[a][1] - ways.at[b][1]),
            )
            for k, a in enumerate(across)
            for b in across[k + 1 :]
        )
    return out, level_of


def walk_of(e: Edge, forward: bool) -> Walk:
    if e.climb is None:
        return Walk(e.metres)
    rise_levels = abs(e.climb) if e.climb == e.climb else 1.0
    slope = hypot(e.metres, rise_levels * DEFAULT_RISE)
    kind = "escalator" if e.escalator else "stairs"
    if e.climb != e.climb:
        # Which end is up is unknown: half each.
        w = Walk(0.0)
        half = slope / 2
        return w.climb(kind, 1, _f(half)).climb(kind, -1, _f(half))
    up = (e.climb > 0) == forward
    return Walk(0.0).climb(kind, 1 if up else -1, _f(slope))


def _f(slope: float):
    from mta_od_data.lidar import Flight

    return Flight(slope, 0.0)


def add(a: Walk, b: Walk) -> Walk:
    return Walk(
        a.metres + b.metres,
        a.stairs_up + b.stairs_up,
        a.stairs_down + b.stairs_down,
        a.escalator_up + b.escalator_up,
        a.escalator_down + b.escalator_down,
    )


def platform_walks(
    outlines: dict[str, Polygon], platform_levels: dict[str, list[float]], ways: Ways
) -> list[tuple[str, str, Walk]]:
    all_edges, level_of = edges(ways)
    es = [e for e in all_edges if e.a not in ways.blocked and e.b not in ways.blocked]
    ids = {n: i for i, n in enumerate(sorted({n for e in es for n in (e.a, e.b)}))}
    arcs: list[tuple[int, int, Walk]] = []
    for e in es:
        arcs.append((ids[e.a], ids[e.b], walk_of(e, True)))
        if e.both:
            arcs.append((ids[e.b], ids[e.a], walk_of(e, False)))
    # Keep the quickest arc between any two nodes.
    best: dict[tuple[int, int], Walk] = {}
    for a, b, w in arcs:
        if (a, b) not in best or w.secs() < best[(a, b)].secs():
            best[(a, b)] = w
    n = len(ids)
    rows = np.array([a for a, _ in best], int)
    cols = np.array([b for _, b in best], int)
    graph = csr_matrix(
        (np.array([max(w.secs(), 1e-3) for w in best.values()]), (rows, cols)), (n, n)
    )
    coords = np.array([ways.at[node] for node in ids])
    order = list(ids)
    seeds = {}
    for way, poly in outlines.items():
        inside = contains_xy(poly.buffer(1.0), coords[:, 0], coords[:, 1])
        if (lv := platform_levels.get(way)) and len(lv) == 1:
            # Its own level's nodes, or untagged ones if it has none.
            # so a platform's nodes aren't those of another stacked over it.
            on_level = np.array([level_of.get(n) == lv[0] for n in order])
            untagged = np.array([n not in level_of for n in order])
            inside &= on_level if (inside & on_level).any() else untagged
        if inside.any():
            seeds[way] = np.nonzero(inside)[0]
    names = list(seeds)
    centre = {w: outlines[w].centroid for w in names}
    tree = STRtree([centre[w] for w in names])
    out = []
    for a in names:
        near = [names[i] for i in tree.query(centre[a].buffer(PAIR_M)) if names[i] != a]
        if not near:
            continue
        dist, pred, _ = dijkstra(
            graph, indices=seeds[a], min_only=True, return_predecessors=True
        )
        for b in near:
            targets = seeds[b]
            t = targets[np.argmin(dist[targets])]
            if not np.isfinite(dist[t]):
                continue
            walk = Walk(0.0)
            node = t
            while pred[node] >= 0:
                walk = add(walk, best[(int(pred[node]), int(node))])
                node = pred[node]
            if walk.metres <= MAX_WALK_M:
                out.append((a, b, walk))
    return out


@app.command()
def osm_walks(
    extract: Annotated[
        Path, Option(help="Geofabrik's New York OSM extract")
    ] = DEFAULT_EXTRACT,
    out: Annotated[
        Path, Option(help="Walks between platforms, for `raptor`")
    ] = DEFAULT_OUT,
) -> None:
    """Walk between each station's platforms along OSM's indoor ways."""
    with open(DEFAULT_AREAS_OUT) as f:
        wanted = {int(r["platform"][1:]) for r in csv.DictReader(f)}
    plats = Platforms(wanted)
    plats.apply_file(str(extract), locations=True)
    ways = Ways(STRtree(list(plats.outlines.values())))
    ways.apply_file(str(extract), locations=True)
    print(
        f"{len(plats.outlines)} platforms, {len(ways.ways)} ways near them, "
        f"{len(ways.blocked)} barrier nodes"
    )
    walks = platform_walks(plats.outlines, plats.levels, ways)
    print(f"{len(walks)} walks between {len({a for a, _, _ in walks})} platforms")
    with open(out, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "from_platform",
                "to_platform",
                "metres",
                "stairs_up_m",
                "stairs_down_m",
                "escalator_up_m",
                "escalator_down_m",
            ]
        )
        w.writerows(
            (a, b, *walk.row()) for a, b, walk in sorted(walks, key=lambda t: t[:2])
        )
