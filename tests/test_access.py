from math import cos, radians
from pathlib import Path

from pytest import approx

from mta_od_data.access import (
    A_DIVISION_FT,
    B_DIVISION_FT,
    GATES_S,
    SIR_FT,
    Walk,
    entrance_secs,
    osm_lengths,
    platform_length,
)


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
    """An OSM file of `ways`, each closed over its corners, whose node `n` is
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
        + "".join(f'<nd ref="{n}"/>' for n in [*ns, ns[0]])
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
    ]
    extract = tmp_path / "platforms.osm"
    _platform_osm(extract, ways)
    platforms = tmp_path / "platforms.csv"
    platforms.write_text("stop,platform\n505,w2\n506,w6\n")
    lengths = osm_lengths(extract, platforms)
    assert lengths["505"] == (approx(150 / 0.3048, rel=1e-3), "w2")
    assert lengths["506"] == (approx(50 / 0.3048, rel=1e-3), "w6")


def test_entrance_secs_stop_where_the_stairs_reach_the_platform():
    # 30 ft of stairs at 1 ft a second, and the fare gates.
    assert entrance_secs("Stair", 30.0, False, None) == 30 + GATES_S
    # A long walk inside the station: 440 ft at 3 mph, then the stairs.
    assert entrance_secs("Stair", 30.0, False, Walk(440, 10, "")) == approx(
        100 + 10 + GATES_S
    )
