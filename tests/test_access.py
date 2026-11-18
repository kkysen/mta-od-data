from math import cos, pi, radians, sin
from pathlib import Path

from pytest import approx
from shapely import Polygon

from mta_od_data.access import (
    A_DIVISION_FT,
    B_DIVISION_FT,
    GATES_S,
    SIR_FT,
    Tracks,
    Walk,
    entrance_secs,
    osm_lengths,
    platform_length,
    track_edges,
)
from mta_od_data.lidar import PlatformAxis


def test_platform_length_from_osm_or_a_full_train():
    osm = {"R31": (629.4, "w510502288")}
    assert platform_length({"gtfs_stop_id": "R31", "division": "BMT"}, osm) == (
        629.4,
        "OSM w510502288",
    )
    irt = {"gtfs_stop_id": "101", "division": "IRT"}
    assert platform_length(irt, osm)[0] == A_DIVISION_FT
    ind = {"gtfs_stop_id": "A01", "division": "IND"}
    assert platform_length(ind, osm)[0] == B_DIVISION_FT
    sir = {"gtfs_stop_id": "S31", "division": "SIR"}
    assert platform_length(sir, osm)[0] == SIR_FT


def _platform_osm(
    path: Path, ways: list[tuple[int, list[int], dict[str, str]]]
) -> None:
    """An OSM file of `ways`, each closed over its corners but tracks, whose node `n` is
    `n // 10` m across the tracks, east, and `n % 10` times 50 m along them, north."""
    lat0, lon0 = 40.85, -73.86
    corners = {n for _, ns, _ in ways for n in ns}
    nodes = [
        f'<node id="{n}" version="1" lat="{lat0 + n % 10 * 50 / 110_540:.7f}" '
        f'lon="{lon0 + n // 10 / (111_320 * cos(radians(lat0))):.7f}"/>'
        for n in sorted(corners)
    ]
    elements = [
        f'<way id="{w}" version="1">'
        + "".join(
            f'<nd ref="{n}"/>'
            for n in (ns if tags.get("railway") == "subway" else [*ns, ns[0]])
        )
        + "".join(f'<tag k="{k}" v="{v}"/>' for k, v in tags.items())
        + "</way>"
        for w, ns, tags in ways
    ]
    path.write_text(
        '<?xml version="1.0"?><osm version="0.6">'
        + "".join(nodes + elements)
        + "</osm>"
    )


def test_osm_lengths_measure_a_platform_mapped_in_pieces_whole(tmp_path: Path):
    # Morris Park's: three pieces 50 m long, split at the tunnel and the bridge,
    # 3 m wide, each sharing its ends' corners with the next.
    platform = {"railway": "platform", "name": "Morris Park", "level": "-1"}
    ways = [
        (1, [0, 30, 31, 1], {**platform, "tunnel": "yes", "layer": "-1"}),
        (2, [1, 31, 32, 2], platform),
        (3, [2, 32, 33, 3], {**platform, "bridge": "yes", "layer": "1"}),
        # Beyond the bridge, the next station's, and a level down, another platform:
        # neither is a piece of it.
        (4, [3, 33, 34, 4], {**platform, "name": "Pelham Pkwy"}),
        (5, [0, 30, 39, 9], {**platform, "level": "-2"}),
        # The platform across the tracks, not touching it.
        (6, [100, 130, 131, 101], platform),
        # The track between them, 2 m east of the first, 5 m west of the other.
        (7, [50, 51, 52, 53, 54, 55], {"railway": "subway"}),
    ]
    extract = tmp_path / "platforms.osm"
    _platform_osm(extract, ways)
    platforms = tmp_path / "platforms.csv"
    platforms.write_text(
        "route,prev_stop,stop,next_stop,direction,platform,trains\n"
        "5,504,505,506,N,w2,100\n5,505,506,,N,w6,100\n"
    )
    stations = tmp_path / "stations.csv"
    stations.write_text("gtfs_stop_id,gtfs_latitude,gtfs_longitude\n")
    lengths = osm_lengths(extract, platforms, stations)
    assert lengths.longest["505"] == (approx(150 / 0.3048, rel=1e-3), "w2")
    assert lengths.longest["506"] == (approx(50 / 0.3048, rel=1e-3), "w6")
    assert lengths.edges["505N", "w2"] == approx(150 / 0.3048, rel=1e-3)


def _tracks(*lines: list[tuple[float, float]]) -> Tracks:
    """Tracks along each of `lines`, a node at each of its points."""
    at: dict[int, tuple[float, float]] = {}
    joined: dict[int, set[int]] = {}
    for line in lines:
        ids = range(len(at), len(at) + len(line))
        at |= dict(zip(ids, line, strict=True))
        for a, b in zip(ids, ids[1:], strict=False):
            joined.setdefault(a, set()).add(b)
            joined.setdefault(b, set()).add(a)
    return Tracks(at, joined)


def _straight(x: float) -> list[tuple[float, float]]:
    """A track `x` m east, north from 100 m south to 250 m north, a node each 10 m."""
    return [(x, y) for y in range(-100, 260, 10)]


def _arc(r: float, a0: float, a1: float, n: int) -> list[tuple[float, float]]:
    """`n` points on a circle of radius `r` about the origin,
    from angle `a0` to `a1`."""
    return [
        (r * cos(a), r * sin(a))
        for a in (a0 + (a1 - a0) * i / (n - 1) for i in range(n))
    ]


def _lengths(outline: Polygon, tracks: Tracks) -> list[float]:
    """`track_edges`' lengths, shortest first."""
    return sorted(e.metres for e in track_edges(outline, tracks))


def test_track_edges_measure_a_straight_platform_end_to_end():
    # 150 m by 4 m, its track 1.6 m to the east.
    rectangle = Polygon([(0, 0), (4, 0), (4, 150), (0, 150)])
    assert _lengths(rectangle, _tracks(_straight(5.6))) == [approx(150)]
    # No track beside it, but one across the way: no edge along a track.
    assert _lengths(rectangle, _tracks(_straight(30))) == []
    # An express track beyond its local, not beside it.
    assert _lengths(rectangle, _tracks(_straight(5.6), _straight(9.3))) == [approx(150)]


def test_track_edges_measure_a_curved_platform_along_its_track_edge():
    # A side platform a 60 degree arc of a 150 m curve, 4 m wide outside it,
    # its track 1.6 m inside, on past both ends.
    theta = pi / 3
    strip = Polygon([*_arc(150, 0, theta, 31), *_arc(154, theta, 0, 31)])
    tracks = _tracks(_arc(148.4, -0.5, theta + 0.5, 80))
    # Along the edge the trains stop at, the inner, 157 m,
    # not straight end to end, 154 m.
    assert _lengths(strip, tracks) == [approx(150 * theta, rel=0.002)]
    assert PlatformAxis.of(strip).length == approx(154)


def test_track_edges_measure_a_jagged_outline_as_a_smooth_one():
    # 150 m by 4 m, its track edge notched 1 m deep every 10 m,
    # and stairs cut 2 m into the back, as OSM draws some.
    edge = [
        p
        for y in range(0, 150, 10)
        for p in [(4, y + 2), (3, y + 4), (3, y + 6), (4, y + 8)]
    ]
    back = [
        p
        for y in range(140, 0, -40)
        for p in [(0, y), (2, y - 5), (2, y - 15), (0, y - 20)]
    ]
    jagged = Polygon([(0, 0), (4, 0), *edge, (4, 150), (0, 150), *back])
    assert _lengths(jagged, _tracks(_straight(5.6))) == [approx(150)]


def test_track_edges_measure_each_of_an_island_platforms_edges():
    # An island 8 m wide on a 60 degree arc of a 150 m curve,
    # a track 1.6 m from each edge.
    theta = pi / 3
    island = Polygon([*_arc(150, 0, theta, 31), *_arc(158, theta, 0, 31)])
    tracks = _tracks(
        _arc(148.4, -0.5, theta + 0.5, 80), _arc(159.6, -0.5, theta + 0.5, 80)
    )
    # The inner edge, along the curve, shorter than the outer.
    assert _lengths(island, tracks) == [
        approx(150 * theta, rel=0.002),
        approx(158 * theta, rel=0.002),
    ]


def test_track_edges_run_on_past_a_terminals_bumpers():
    # The track ends 10 m short of the platform's far end.
    rectangle = Polygon([(0, 0), (4, 0), (4, 150), (0, 150)])
    assert _lengths(rectangle, _tracks(_straight(5.6)[:25])) == [approx(150)]


LAT0, LON0 = 40.85, -73.86


def _lon_lat(x: float, y: float) -> tuple[float, float]:
    """The point `x` m east and `y` m north of `LAT0`, `LON0`."""
    return LON0 + x / (111_320 * cos(radians(LAT0))), LAT0 + y / 110_540


def test_osm_lengths_give_each_direction_its_islands_edge(tmp_path: Path):
    # B's island, a 60 degree arc of a 150 m curve 8 m wide,
    # its tracks 1.6 m inside and outside it;
    # northbound, counterclockwise, on the outer, as its route's relation stops,
    # and southbound on the inner. A and C are the stations before and after.
    theta = pi / 3
    nodes: list[tuple[float, float]] = []

    def at(x: float, y: float) -> int:
        nodes.append((x, y))
        return len(nodes)

    def arc(r: float, a0: float, a1: float, n: int) -> list[int]:
        return [at(x, y) for x, y in _arc(r, a0, a1, n)]

    island = arc(150, 0, theta, 31) + arc(158, theta, 0, 31)
    outer = arc(159.6, -0.6, theta + 0.6, 121)
    inner = arc(148.4, -0.6, theta + 0.6, 121)
    # C's platforms, a stretch on, each beside its track's last node.
    beyond = {
        track[-1]: [at(x + dx, y + dy) for dx, dy in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        for track in (outer, inner)
        for x, y in [nodes[track[-1] - 1]]
    }

    def way(i: int, ns: list[int], tags: dict[str, str]) -> str:
        return (
            f'<way id="{i}" version="1">'
            + "".join(f'<nd ref="{n}"/>' for n in ns)
            + "".join(f'<tag k="{k}" v="{v}"/>' for k, v in tags.items())
            + "</way>"
        )

    def route(i: int, stops: list[tuple[int, int]]) -> str:
        return (
            f'<relation id="{i}" version="1">'
            + "".join(
                f'<member type="node" ref="{n}" role="stop"/>'
                f'<member type="way" ref="{w}" role="platform"/>'
                for n, w in stops
            )
            + '<tag k="type" v="route"/><tag k="route" v="subway"/>'
            '<tag k="network" v="NYC Subway"/><tag k="ref" v="1"/></relation>'
        )

    platform = {"railway": "platform", "name": "B"}
    middle = 60  # Of each track's 121 nodes, at 30 degrees.
    elements = [
        way(1, [*island, island[0]], platform),
        way(2, outer, {"railway": "subway"}),
        way(3, inner, {"railway": "subway"}),
        *(
            way(4 + i, [*ns, ns[0]], {"railway": "platform", "name": "C"})
            for i, ns in enumerate(beyond.values())
        ),
        route(1, [(outer[middle], 1), (outer[-1], 4)]),
        route(2, [(inner[-1], 5), (inner[middle], 1)]),
    ]
    extract = tmp_path / "platforms.osm"
    extract.write_text(
        '<?xml version="1.0"?><osm version="0.6">'
        + "".join(
            f'<node id="{i}" version="1" lat="{lat:.8f}" lon="{lon:.8f}"/>'
            for i, (lon, lat) in enumerate((_lon_lat(x, y) for x, y in nodes), start=1)
        )
        + "".join(elements)
        + "</osm>"
    )
    platforms = tmp_path / "platforms.csv"
    platforms.write_text(
        "route,prev_stop,stop,next_stop,direction,platform,trains\n"
        "1,A,B,C,N,w1,100\n1,C,B,A,S,w1,100\n"
    )
    stations = tmp_path / "stations.csv"
    stations.write_text(
        "gtfs_stop_id,gtfs_latitude,gtfs_longitude\n"
        + "".join(
            f"{s},{lat},{lon}\n"
            for s, a in [("A", -0.4), ("B", theta / 2), ("C", theta + 0.4)]
            for lon, lat in [_lon_lat(154 * cos(a), 154 * sin(a))]
        )
    )
    lengths = osm_lengths(extract, platforms, stations)
    assert lengths.edges["BN", "w1"] == approx(158 * theta / 0.3048, rel=0.003)
    assert lengths.edges["BS", "w1"] == approx(150 * theta / 0.3048, rel=0.003)
    # For its stops whose platform isn't known, its longest.
    assert lengths.longest["B"] == (approx(158 * theta / 0.3048, rel=0.003), "w1")


def test_entrance_secs_stop_where_the_stairs_reach_the_platform():
    # 30 ft of stairs at 1 ft a second, and the fare gates.
    assert entrance_secs("Stair", 30.0, False, None) == 30 + GATES_S
    # A long walk inside the station: 440 ft at 3 mph, then the stairs.
    assert entrance_secs("Stair", 30.0, False, Walk(440, 10, "")) == approx(
        100 + 10 + GATES_S
    )
