from shapely.geometry import Polygon

from mta_od_data.osm_walks import level_changes


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
