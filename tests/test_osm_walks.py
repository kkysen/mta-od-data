from shapely import STRtree
from shapely.geometry import Polygon

from mta_od_data.osm_walks import Ways, level_changes, platform_walks, way_of_areas


def floor(level: str, ring: list[int], corners: list[tuple[float, float]], **tags: str):
    return ({"indoor": "area", "level": level, **tags}, ring, Polygon(corners))


def test_floors_a_level_apart_sharing_a_side_join_along_it() -> None:
    # A passage on -1, 0 to 10 m, then on -2, 10 to 20 m, sharing the side at 10 m.
    upper = floor("-1", [1, 2, 3, 4], [(0, 0), (10, 0), (10, 5), (0, 5)])
    lower = floor("-2", [2, 5, 6, 3], [(10, 0), (20, 0), (20, 5), (10, 5)])
    assert sorted(level_changes([upper, lower])) == [(2, -2.0, -1.0), (3, -2.0, -1.0)]


def test_stacked_floors_platforms_and_two_levels_apart_dont() -> None:
    upper = floor("-1", [1, 2, 3, 4], [(0, 0), (10, 0), (10, 5), (0, 5)])
    # Right under it, sharing a side: a mezzanine over a lower floor.
    under = floor("-2", [1, 2, 7, 8], [(0, 0), (10, 0), (10, 4), (0, 4)])
    platform = floor(
        "-2", [2, 5, 6, 3], [(10, 0), (20, 0), (20, 5), (10, 5)], railway="platform"
    )
    deeper = floor("-3", [2, 5, 6, 3], [(10, 0), (20, 0), (20, 5), (10, 5)])
    assert level_changes([upper, under]) == []
    assert level_changes([upper, platform]) == []
    assert level_changes([upper, deeper]) == []


def test_a_flight_runs_up_to_the_end_only_on_its_upper_level() -> None:
    # Node 1 is only by an area on -1, node 2 by areas on both.
    by = {(1, -1.0), (2, -1.0), (2, -2.0)}

    def within(n: int, level: float) -> list[int]:
        return [0] if (n, level) in by else []

    assert way_of_areas(within, 1, 2, -2.0, -1.0) == -1.0
    assert way_of_areas(within, 2, 1, -2.0, -1.0) == 1.0
    # Both ends by both levels, or neither: it can't tell.
    assert way_of_areas(within, 2, 2, -2.0, -1.0) == 0.0
    assert way_of_areas(within, 3, 4, -2.0, -1.0) == 0.0


def rect(
    ids: list[int],
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    at: dict[int, tuple[float, float]],
):
    for n, p in zip(ids, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], strict=True):
        at[n] = p
    return [*ids, ids[0]]


def test_flights_drawn_top_first_with_no_incline_join_the_platforms() -> None:
    """Two platforms on -2 across the tracks from each other,
    a mezzanine on -1 over the tracks between them,
    and a flight down to each, drawn from its top, in the mezzanine only,
    to its bottom, in the mezzanine and on the platform, with no `incline`."""
    at: dict[int, tuple[float, float]] = {}
    south = rect([1, 2, 3, 4], 0, 0, 40, 5, at)
    north = rect([5, 6, 7, 8], 0, 25, 40, 30, at)
    mezzanine = rect([9, 10, 11, 12], 0, 4, 40, 26, at)
    at |= {20: (10, 12), 21: (10, 3), 22: (30, 18), 23: (30, 27)}
    ways = Ways(STRtree([]))
    ways.at = at
    ways.ways = [
        (1, {"railway": "platform", "level": "-2"}, south),
        (2, {"railway": "platform", "level": "-2"}, north),
        (3, {"indoor": "area", "level": "-1"}, mezzanine),
        (4, {"highway": "steps", "level": "-2;-1"}, [20, 21]),
        (5, {"highway": "steps", "level": "-2;-1"}, [22, 23]),
    ]
    outlines = {
        f"w{i}": Polygon([at[n] for n in ring]) for i, ring in ((1, south), (2, north))
    }
    walks = platform_walks(outlines, {"w1": [-2.0], "w2": [-2.0]}, ways)
    assert {(a, b) for a, b, _ in walks} == {("w1", "w2"), ("w2", "w1")}
    for _, _, way in walks:
        assert way.walk.stairs_up > 0
        assert way.walk.stairs_down > 0
