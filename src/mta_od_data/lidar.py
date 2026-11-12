"""Walks between a station's platforms, measured off Sabrina Mielke's LiDAR station maps
(CC BY-SA 4.0, https://commons.wikimedia.org/wiki/User:Sjmielke),
for `raptor`'s transfers, over any other source (`raptor/lidar_walks.csv`).

Each map's main view is a parallel projection of the station,
traced from iPhone LiDAR scans:
a point on the ground lands at `A @ (east, north) + b`,
raised up the page by its depth, an offset a platform.
`A` and the offsets are fitted to OSM's outlines of the platforms,
matching each platform's full-width ends on the map to its outline's;
the forked tips past them, back of house, are left out.
A level ground plane viewed from above at an angle fits as well as any affine map,
so the fit is the view, not a distortion of it.

Along each platform, the stairs and escalators touching it are found by color:
gray steps, black escalators, wider than the map's dashed drop lines.
Each meets the platform at its foot, the end of it lowest on the page.
Stairs off the N/Q/R/W rise to the upper mezzanine, and off the 7 to the lower;
the 1/2/3's go both ways, so theirs were read one by one
(`lidar_maps/times_sq_123_connectors.csv`).

A walk between two platforms is the quickest over a connector off each
reaching mezzanines: the straight line between their feet,
and the levels climbed and descended, which `raptor` times
(`raptor/src/lidar.rs`).
It assumes a rider on the car nearest the connector;
where else on the train riders are is left for later.
"""

import csv
import json
from dataclasses import dataclass
from itertools import permutations, product
from pathlib import Path
from typing import Annotated

import numpy as np
import osmium
from osmium.osm import Way
from PIL import Image
from scipy import ndimage
from shapely import Polygon, contains_xy
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.platforms import DEFAULT_EXTRACT

app = Typer()

MAPS_DIR = DATA / "station-maps-lidar"
TABLES = Path(__file__).parent / "lidar_maps"
DEFAULT_OUT = Path(__file__).parents[2] / "raptor" / "lidar_walks.csv"
CACHE = Path(__file__).parents[2] / "target" / "lidar"

# `raptor`'s walking speed in a station, and a flight of stairs a level,
# to pick the quickest pair of connectors.
WALK_M_PER_S = 1.2
FLIGHT_SECS = 30
# The maps are read at a quarter of their size: a pixel is still under 10 cm.
REDUCE = 4
# How far apart, across them, a color's platforms at one station are
# on the reduced map, at most.
MAX_ISLAND_SPREAD = 400


@dataclass(frozen=True, slots=True)
class MapPlatform:
    """A platform on a map: its OSM way, its color on the map, and its group,
    the platforms drawn at one depth together."""

    way: str
    color: str
    group: str
    level: int
    # The mezzanine level every connector off it reaches, if all reach one.
    reaches: int | None


@dataclass(frozen=True, slots=True)
class StationMap:
    name: str
    file: str
    # Rows of the full-size map holding the main view, not its insets.
    main_rows: int
    platforms: tuple[MapPlatform, ...]
    # Connectors read one by one, for platforms whose `reaches` is `None`.
    table: str | None


TIMES_SQ = StationMap(
    name="Times Square-42nd Street",
    file="Times Square–42nd Street (NYC subway station map).png",
    main_rows=19360,
    platforms=(
        MapPlatform("w513706097", "red", "123", -2, None),
        MapPlatform("w513706098", "red", "123", -2, None),
        MapPlatform("w513706124", "yellow", "nqrw", -2, -1),
        MapPlatform("w513706125", "yellow", "nqrw", -2, -1),
        MapPlatform("w513706084", "magenta", "7", -4, -3),
    ),
    table="times_sq_123_connectors.csv",
)
MAPS = (TIMES_SQ,)


def colour_mask(img: np.ndarray, color: str) -> np.ndarray:
    r, g, b = (img[..., i].astype(np.int16) for i in range(3))
    match color:
        case "red":
            return (r > 150) & (r - g > 100) & (b < 90)
        case "yellow":
            return (
                (abs(r - 212) < 30)
                & (abs(g - 192) < 30)
                & (abs(b - 119) < 35)
                & (r - b > 60)
            )
        case "magenta":
            return (r > 150) & (b > 140) & (r - g > 50) & (b - g > 40)
    raise ValueError(color)


def load_map(m: StationMap) -> np.ndarray:
    """The main view, at a quarter size, cached in `target/lidar/`."""
    cached = CACHE / f"{Path(m.file).stem}.npy"
    if cached.exists():
        return np.load(cached)[: m.main_rows // REDUCE]
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(MAPS_DIR / m.file) as im:
        im = im.convert("RGB")
        img = np.asarray(im.reduce(REDUCE))[: m.main_rows // REDUCE]
    CACHE.mkdir(parents=True, exist_ok=True)
    np.save(cached, img)
    return img


def axis(pts: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Mean, principal axis (pointing right),
    and cross axis (pointing down the page)."""
    mean = pts.mean(0)
    _, _, vt = np.linalg.svd(pts - mean, full_matrices=False)
    return mean, vt[0] * np.sign(vt[0][0]), vt[1] * np.sign(vt[1][1])


def full_width_ends(pts: np.ndarray, step: float) -> np.ndarray:
    """The two ends of a platform's full-width part, on its centerline."""
    mean, ax, cr = axis(pts)
    s = (pts - mean) @ ax
    t = (pts - mean) @ cr
    counts = np.bincount(((s - s.min()) / step).astype(int))
    full = np.nonzero(counts >= 0.8 * np.median(counts[counts > 0]))[0]
    s0 = s.min() + full[0] * step
    s1 = s.min() + (full[-1] + 1) * step
    centre = mean + np.median(t[(s >= s0) & (s <= s1)]) * cr
    return np.array([centre + s0 * ax, centre + s1 * ax])


def split_by_colour(img: np.ndarray, m: StationMap) -> dict[str, np.ndarray]:
    """Each platform's pixels, in full-size map coordinates:
    the largest pieces of its color, as many as it has platforms,
    told apart across their shared axis by 2-means."""
    out = {}
    for color in dict.fromkeys(p.color for p in m.platforms):
        ways = [p.way for p in m.platforms if p.color == color]
        mask = colour_mask(img, color)
        lab, n = ndimage.label(ndimage.binary_closing(mask, iterations=3))
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        biggest = np.argsort(-sizes)[:10] + 1
        # Pieces at least a fifth the biggest, along its line:
        # one platform split by what's drawn over it,
        # not another line of the same color.
        ys, xs = np.nonzero(lab == biggest[0])
        mean, _, cr = axis(np.stack([xs, ys], 1).astype(float))
        keep = []
        for i in biggest:
            if sizes[i - 1] < sizes[biggest[0] - 1] / 5:
                continue
            ys, xs = np.nonzero(lab == i)
            if abs((np.array([xs.mean(), ys.mean()]) - mean) @ cr) < MAX_ISLAND_SPREAD:
                keep.append(i)
        ys, xs = np.nonzero(np.isin(lab, keep) & mask)
        pts = np.stack([xs, ys], 1).astype(float) * REDUCE
        if len(ways) == 1:
            out[ways[0]] = pts
            continue
        mean, _, cr = axis(pts)
        t = (pts - mean) @ cr
        lo, hi = np.percentile(t, 25), np.percentile(t, 75)
        for _ in range(30):
            cut = (lo + hi) / 2
            lo, hi = t[t < cut].mean(), t[t >= cut].mean()
        # Matched to ways by the fit, which tries each order.
        out[f"{color}:0"] = pts[t < cut]
        out[f"{color}:1"] = pts[t >= cut]
    return out


class Outlines(osmium.SimpleHandler):
    def __init__(self, ways: set[int]) -> None:
        super().__init__()
        self.ways = ways
        self.outlines: dict[str, list[tuple[float, float]]] = {}

    def way(self, w: Way) -> None:
        if w.id in self.ways:
            self.outlines[f"w{w.id}"] = [(n.lon, n.lat) for n in w.nodes]


def ground_points(
    outline: list[tuple[float, float]], origin: tuple[float, float]
) -> np.ndarray:
    """A grid of points 10 cm apart inside an outline,
    in metres east and north of `origin`."""
    lon0, lat0 = origin
    p = np.array(outline)
    xy = np.stack(
        [
            (p[:, 0] - lon0) * 111_320 * np.cos(np.radians(lat0)),
            (p[:, 1] - lat0) * 110_540,
        ],
        1,
    )
    poly = Polygon(xy)
    x0, y0, x1, y1 = poly.bounds
    gx, gy = np.meshgrid(np.arange(x0, x1, 0.1), np.arange(y0, y1, 0.1))
    inside = contains_xy(poly, gx, gy)
    return np.stack([gx[inside], gy[inside]], 1)


@dataclass(frozen=True, slots=True)
class Projection:
    a: np.ndarray
    b: np.ndarray
    offsets: dict[str, float]
    rms_px: float
    # Which map piece is which way.
    pieces: dict[str, str]

    def to_ground(self, pxy: np.ndarray, group: str) -> np.ndarray:
        return np.linalg.solve(
            self.a, np.asarray(pxy) - self.b - [0, self.offsets[group]]
        )


def fit(
    m: StationMap, pieces: dict[str, np.ndarray], ground: dict[str, np.ndarray]
) -> Projection:
    """The projection fitting the platforms' full-width ends best,
    over each way to match the pieces of a color to its ways
    and each piece's ends to its outline's."""
    by_way = {p.way: p for p in m.platforms}
    groups = list(dict.fromkeys(p.group for p in m.platforms))
    gends = {w: full_width_ends(g, 0.1) for w, g in ground.items()}
    pends = {k: full_width_ends(v, REDUCE) for k, v in pieces.items()}
    colors = list(dict.fromkeys(p.color for p in m.platforms))
    choices = []
    for color in colors:
        ways = [p.way for p in m.platforms if p.color == color]
        if len(ways) == 1:
            choices.append([{ways[0]: ways[0]}])
        else:
            choices.append(
                [
                    {f"{color}:{i}": w for i, w in enumerate(order)}
                    for order in permutations(ways)
                ]
            )
    best = None
    for combo in product(*choices):
        match = {k: v for c in combo for k, v in c.items()}
        keys = list(match)
        for flips in product((0, 1), repeat=len(keys)):
            rows: list[np.ndarray] = []
            rhs: list[float] = []
            for k, f in zip(keys, flips, strict=True):
                gi = groups.index(by_way[match[k]].group)
                for j in (0, 1):
                    g = gends[match[k]][j ^ f]
                    for dim in (0, 1):
                        row = np.zeros(6 + len(groups) - 1)
                        row[2 * dim : 2 * dim + 2] = g
                        row[4 + dim] = 1
                        if dim == 1 and gi > 0:
                            row[5 + gi] = 1
                        rows.append(row)
                        rhs.append(pends[k][j][dim])
            mat, y = np.array(rows), np.array(rhs)
            sol, *_ = np.linalg.lstsq(mat, y, rcond=None)
            rms = float(np.sqrt(((mat @ sol - y).reshape(-1, 2) ** 2).sum(1).mean()))
            if best is None or rms < best[0]:
                best = (rms, sol, match)
    assert best is not None, "a map has platforms"
    rms, sol, match = best
    offsets = {groups[0]: 0.0} | {
        g: float(sol[5 + i]) for i, g in enumerate(groups) if i > 0
    }
    return Projection(sol[:4].reshape(2, 2), sol[4:6], offsets, rms, match)


def feet(
    img: np.ndarray, pts: np.ndarray, platform_mask: np.ndarray
) -> list[tuple[str, np.ndarray]]:
    """Each stair or escalator touching a platform, by kind,
    and where its foot meets the platform,
    in full-size map coordinates."""
    r, g, b = (img[..., i].astype(np.int16) for i in range(3))
    grey = (abs(r - g) < 16) & (abs(g - b) < 16)
    steps = grey & (r >= 60) & (r < 200)
    black = (r < 60) & (g < 60) & (b < 60)
    q = pts / REDUCE
    mean, ax, cr = axis(q)
    s = (q - mean) @ ax
    t = (q - mean) @ cr
    top, bottom = np.percentile(t, 2), np.percentile(t, 98)
    above = 70
    ss = np.arange(s.min(), s.max())
    tt = np.arange(top - above, bottom)
    x = np.clip(
        (mean[0] + ss[:, None] * ax[0] + tt[None, :] * cr[0]).round().astype(int),
        0,
        img.shape[1] - 1,
    )
    y = np.clip(
        (mean[1] + ss[:, None] * ax[1] + tt[None, :] * cr[1]).round().astype(int),
        0,
        img.shape[0] - 1,
    )
    # Dashed drop lines are thin; stairs are wide.
    conn = ndimage.binary_opening((steps | black)[y, x], np.ones((4, 4)))
    lab, n = ndimage.label(conn)
    out = []
    for i in range(1, n + 1):
        si, ti = np.nonzero(lab == i)
        if len(si) < 150 or si.max() - si.min() < 12 or ti.max() < above - 2:
            continue
        # A translucent elevator shaft is lighter gray than stairs.
        on = (y[si, ti], x[si, ti])
        if r[on].mean() > 175:
            continue
        kind = "escalator" if black[on].mean() > 0.5 else "stairs"
        foot = si[ti >= np.percentile(ti, 97)]
        s_foot = ss[int(round(foot.mean()))]
        out.append((kind, (mean + s_foot * ax) * REDUCE))
    return out


@dataclass(frozen=True, slots=True)
class Connector:
    way: str
    east: float
    north: float
    reaches: int
    kind: str


def connectors(m: StationMap, extract: Path) -> tuple[list[Connector], Projection]:
    img = load_map(m)
    pieces = split_by_colour(img, m)
    handler = Outlines({int(p.way[1:]) for p in m.platforms})
    handler.apply_file(str(extract), locations=True)
    first = handler.outlines[m.platforms[0].way][0]
    ground = {w: ground_points(o, first) for w, o in handler.outlines.items()}
    proj = fit(m, pieces, ground)
    by_way = {p.way: p for p in m.platforms}
    out = []
    for piece, way in proj.pieces.items():
        p = by_way[way]
        if p.reaches is None:
            continue
        for kind, pxy in feet(img, pieces[piece], colour_mask(img, p.color)):
            e, n = proj.to_ground(pxy, p.group)
            out.append(Connector(way, float(e), float(n), p.reaches, kind))
    if m.table:
        with open(TABLES / m.table) as f:
            for row in csv.DictReader(f):
                if row["kind"] == "elevator":
                    continue
                p = by_way[row["osm_way"]]
                for x, y in zip(
                    row["landing_x"].split(";"),
                    row["landing_y"].split(";"),
                    strict=True,
                ):
                    e, n = proj.to_ground(np.array([float(x), float(y)]), p.group)
                    reaches = p.level + (1 if row["goes"] == "up" else -1)
                    out.append(
                        Connector(p.way, float(e), float(n), reaches, row["kind"])
                    )
    return out, proj


def walks(
    m: StationMap, conns: list[Connector]
) -> list[tuple[str, str, float, int, int]]:
    """The quickest walk between every two platforms, each way:
    `(from, to, metres, levels up, levels down)`,
    picked at `WALK_M_PER_S` and `FLIGHT_SECS` a level,
    which `raptor` times them by its own speeds."""
    level = {p.way: p.level for p in m.platforms}
    out = []
    for a, b in permutations(level, 2):
        best = None
        for c in (c for c in conns if c.way == a):
            for d in (d for d in conns if d.way == b):
                steps = (
                    c.reaches - level[a],
                    d.reaches - c.reaches,
                    level[b] - d.reaches,
                )
                up = sum(x for x in steps if x > 0)
                down = -sum(x for x in steps if x < 0)
                metres = float(np.hypot(c.east - d.east, c.north - d.north))
                secs = metres / WALK_M_PER_S + (up + down) * FLIGHT_SECS
                if best is None or secs < best[0]:
                    best = (secs, (a, b, round(metres, 1), up, down))
        if best:
            out.append(best[1])
    return out


@app.command()
def lidar_walks(
    extract: Annotated[
        Path, Option(help="Geofabrik's New York OSM extract")
    ] = DEFAULT_EXTRACT,
    out: Annotated[
        Path, Option(help="Walks between platforms, for `raptor`")
    ] = DEFAULT_OUT,
) -> None:
    """Measure walks between each mapped station's platforms
    off Sabrina Mielke's LiDAR maps."""
    rows = []
    for m in MAPS:
        conns, proj = connectors(m, extract)
        print(
            f"{m.name}: fit to OSM within {proj.rms_px:.0f} px RMS, "
            f"{len(conns)} connectors, pieces {json.dumps(proj.pieces)}"
        )
        rows.extend((*w, m.name) for w in walks(m, conns))
    with open(out, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "from_platform",
                "to_platform",
                "metres",
                "levels_up",
                "levels_down",
                "station",
            ]
        )
        w.writerows(rows)
