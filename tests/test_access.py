from pytest import approx

from mta_od_data.access import (
    A_DIVISION_FT,
    B_DIVISION_FT,
    GATES_S,
    SIR_FT,
    Walk,
    entrance_secs,
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


def test_entrance_secs_stop_where_the_stairs_reach_the_platform():
    # 30 ft of stairs at 1 ft a second, and the fare gates.
    assert entrance_secs("Stair", 30.0, False, None) == 30 + GATES_S
    # A long walk inside the station: 440 ft at 3 mph, then the stairs.
    assert entrance_secs("Stair", 30.0, False, Walk(440, 10, "")) == approx(
        100 + 10 + GATES_S
    )
