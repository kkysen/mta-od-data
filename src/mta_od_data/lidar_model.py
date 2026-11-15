"""Text extracts of Sabrina Mielke's 3D station models
(CC BY-SA 4.0, https://commons.wikimedia.org/wiki/User:Sjmielke),
the Blender models she fitted to her iPhone LiDAR scans
and drew her station maps from (`lidar`).

A model is in metres, `z` up, at true heights where its levels aren't drawn apart,
in its own frame, not tied to the ground: `lidar` fits it to OSM.
Its floors are filled outlines (Blender curves) at their heights,
tilted for slopes and ramps,
and its stairs and escalators are meshes, mostly one step repeated (Array modifiers).
Every object is named, like `Q mezzanine` or `stairs L->Q dt bot`,
and floors outside the fare gates are named `outside` or `street`.

The extract keeps, in each object's place in the model (Blender's world space):
- each curve's outlines, as Blender draws them, within a centimetre;
- each mesh's bounds, and the middles of its lowest and highest points,
  a stair's foot and top, with its Array modifiers applied;
- each object's collections, and any modifiers it doesn't apply.

The `.blend` files themselves aren't checked in,
as they're binary and weren't published; their extracts are, in `lidar_maps/`.
"""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Annotated, Any

import numpy as np
from typer import Argument, Option, Typer

from mta_od_data.blend import Blend, Block

app = Typer()

TABLES = Path(__file__).parent / "lidar_maps"
# Blender's object types: mesh and curve.
OB_MESH = 1
OB_CURVE = 2
# A curve's spline that closes on itself.
CU_NURB_CYCLIC = 1
# Array modifier offsets: constant, relative to its mesh's size, and by an object.
ARRAY_CONSTANT = 1
ARRAY_RELATIVE = 2
ARRAY_OBJECT = 4
ARRAY_FIXED_COUNT = 0
# A mesh's foot and top: the middle of its points this near its lowest and highest.
END_M = 0.25
# Rounded to the centimetre, and outlines kept within a centimetre
# of Blender's, with as few points as that needs.
DECIMALS = 2
TOLERANCE_M = 0.01


def world(ob: Block, b: Blend) -> np.ndarray:
    """An object's transform to world space, from its saved matrix,
    which Blender stores column by column."""
    return np.array(b.floats(ob, "obmat")).reshape(4, 4).T


def apply(m: np.ndarray, pts: np.ndarray) -> np.ndarray:
    return (np.c_[pts, np.ones(len(pts))] @ m.T)[:, :3]


def bezier(knots: np.ndarray, cyclic: bool, resolution: int) -> np.ndarray:
    """A Bézier spline's points, `resolution` a segment, as Blender draws it,
    from its knots' `(left handle, point, right handle)`."""
    n = len(knots)
    t = np.linspace(0, 1, resolution, endpoint=False)[:, None]
    out = []
    for i in range(n if cyclic else n - 1):
        a, b = knots[i, 1], knots[i, 2]
        c, d = knots[(i + 1) % n, 0], knots[(i + 1) % n, 1]
        out.append(
            (1 - t) ** 3 * a
            + 3 * (1 - t) ** 2 * t * b
            + 3 * (1 - t) * t**2 * c
            + t**3 * d
        )
    if not cyclic:
        out.append(knots[-1:, 1])
    return np.vstack(out)


def simplify(pts: np.ndarray) -> np.ndarray:
    """Ramer-Douglas-Peucker: the fewest of a line's points
    keeping it within `TOLERANCE_M` of all of them."""
    keep = np.zeros(len(pts), bool)
    keep[[0, -1]] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, d = pts[i], pts[j] - pts[i]
        rel = pts[i + 1 : j] - a
        length = np.linalg.norm(d)
        off = (
            np.linalg.norm(np.cross(rel, d), axis=1) / length
            if length > 0
            else np.linalg.norm(rel, axis=1)
        )
        k = int(np.argmax(off))
        if off[k] > TOLERANCE_M:
            keep[i + 1 + k] = True
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return pts[keep]


def curve_rings(ob: Block, b: Blend) -> list[np.ndarray]:
    data = b.at[b.integer(ob, "data")]
    rings = []
    for nurb in b.chain(b.integer(data, "nurb.first")):
        n = b.integer(nurb, "pntsu")
        cyclic = bool(b.integer(nurb, "flagu") & CU_NURB_CYCLIC)
        match b.integer(nurb, "type"):
            case 1:  # CU_BEZIER
                bez = b.at[b.integer(nurb, "bezt")]
                knots = np.array([b.floats(bez, "vec", i) for i in range(n)])
                pts = bezier(knots.reshape(n, 3, 3), cyclic, b.integer(nurb, "resolu"))
            case 0:  # CU_POLY
                bp = b.at[b.integer(nurb, "bp")]
                pts = np.array([b.floats(bp, "vec", i)[:3] for i in range(n)])
            case t:  # NURBS aren't read.
                name = b.text(ob, "id.name")[2:]
                raise ValueError(f"{name}: curve type {t} isn't read")
        pts = apply(world(ob, b), pts)
        # A closed one's first point is kept as its last too.
        closed = np.vstack([pts, pts[:1]]) if cyclic else pts
        rings.append(simplify(closed)[:-1] if cyclic else simplify(closed))
    return rings


def mesh_points(ob: Block, b: Blend) -> np.ndarray:
    """A mesh's points, in its own frame, from its `position` attribute,
    as Blender 4 saves them."""
    data = b.at[b.integer(ob, "data")]
    n = b.integer(data, "totvert")
    layers = b.at[b.integer(data, "vdata.layers")]
    for i in range(b.integer(data, "vdata.totlayer")):
        if b.text(layers, "name", i) == "position":
            raw = b.bytes_at(b.integer(layers, "data", i))
            return np.frombuffer(raw, "<f4")[: 3 * n].reshape(n, 3).astype(float)
    name = b.text(ob, "id.name")[2:]
    raise ValueError(f"{name}: no `position` attribute; saved before Blender 3.5?")


def modifiers(ob: Block, b: Blend) -> list[Block]:
    return b.chain(b.integer(ob, "modifiers.first"), "modifier.next")


def array(pts: np.ndarray, mod: Block, b: Blend) -> np.ndarray | None:
    """A mesh's points repeated by an Array modifier with a fixed count,
    or `None` if it fits a length or is offset by another object,
    as a turnstile's struts turn about its hub.
    Its `scale` is the relative offset, in multiples of the mesh's size."""
    kinds = b.integer(mod, "offset_type")
    if b.integer(mod, "fit_type") != ARRAY_FIXED_COUNT or kinds & ARRAY_OBJECT:
        return None
    step = np.zeros(3)
    if kinds & ARRAY_CONSTANT:
        step += b.floats(mod, "offset")
    if kinds & ARRAY_RELATIVE:
        step += np.array(b.floats(mod, "scale")) * (pts.max(0) - pts.min(0))
    return np.vstack([pts + k * step for k in range(b.integer(mod, "count"))])


def rounded(a: np.ndarray) -> list[Any]:
    return np.round(a, DECIMALS).tolist()


def extract(path: Path) -> dict[str, Any]:
    b = Blend(path)
    collections: defaultdict[str, list[str]] = defaultdict(list)
    for gr in b.blocks[b"GR"]:
        for co in b.chain(b.integer(gr, "gobject.first")):
            ob = b.at[b.integer(co, "ob")]
            collections[b.text(ob, "id.name")[2:]].append(b.text(gr, "id.name")[2:])
    curves = []
    meshes = []
    for ob in sorted(b.blocks[b"OB"], key=lambda ob: b.text(ob, "id.name")):
        name = b.text(ob, "id.name")[2:]
        kind = b.integer(ob, "type")
        if kind not in (OB_MESH, OB_CURVE):
            continue
        unapplied = []
        common: dict[str, Any] = {
            "name": name,
            "collections": sorted(collections[name]),
        }
        if kind == OB_CURVE:
            unapplied = [b.text(m, "modifier.name") for m in modifiers(ob, b)]
            rings = curve_rings(ob, b)
            curves.append(
                common
                | ({"unapplied": unapplied} if unapplied else {})
                | {"rings": [rounded(r) for r in rings]}
            )
            continue
        pts = mesh_points(ob, b)
        steps = None
        for m in modifiers(ob, b):
            if (
                m.struct.name == "ArrayModifierData"
                and (repeated := array(pts, m, b)) is not None
            ):
                steps = b.integer(m, "count")
                pts = repeated
            else:
                unapplied.append(b.text(m, "modifier.name"))
        if len(pts) == 0:
            continue
        pts = apply(world(ob, b), pts)
        lo, hi = pts[:, 2].min(), pts[:, 2].max()
        meshes.append(
            common
            | ({"unapplied": unapplied} if unapplied else {})
            | ({"steps": steps} if steps is not None else {})
            | {
                "min": rounded(pts.min(0)),
                "max": rounded(pts.max(0)),
                "foot": rounded(pts[pts[:, 2] < lo + END_M].mean(0)),
                "top": rounded(pts[pts[:, 2] > hi - END_M].mean(0)),
            }
        )
    return {
        "source": path.name,
        "credit": "Sabrina Mielke, CC BY-SA 4.0",
        "curves": curves,
        "meshes": meshes,
    }


def dumps(model: dict[str, Any]) -> str:
    """JSON with a point a line, for small diffs."""
    text = json.dumps(model, indent=1, ensure_ascii=False)
    num = r"-?\d+(?:\.\d+)?(?:e-?\d+)?"
    return (
        re.sub(rf"\[\s*({num}),\s*({num}),\s*({num})\s*\]", r"[\1, \2, \3]", text)
        + "\n"
    )


@app.command()
def lidar_model(
    blend: Annotated[Path, Argument(help="A station's `.blend` model")],
    out: Annotated[
        Path | None,
        Option(help="Its extract; by default `lidar_maps/<its name>.json`"),
    ] = None,
) -> None:
    """Extract a station's floors, stairs and escalators
    from Sabrina Mielke's Blender model of it."""
    model = extract(blend)
    out = out or TABLES / f"{blend.stem}.json"
    out.write_text(dumps(model))
    print(f"{out}: {len(model['curves'])} curves, {len(model['meshes'])} meshes")
