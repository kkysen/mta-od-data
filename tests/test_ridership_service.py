from mta_od_data.ridership.service import Pattern, route_length, segment_lengths


def pattern(route: str, stops: str, lengths: list[float]) -> Pattern:
    return Pattern(route, "Weekday", tuple(stops.split()), tuple(lengths))


def test_route_length_counts_regular_local_track_once() -> None:
    local = pattern("6", "a b c d", [1.0, 1.0, 1.0])
    # Express over the local's track: skips `b` and `c`, so adds nothing.
    express = pattern("6X", "a d e", [2.5, 4.0])
    # A rare extension: under `REGULAR_SHARE` of the 6's trips.
    extension = pattern("6", "a b c d f", [1.0, 1.0, 1.0, 8.0])
    patterns = {local: 95, express: 50, extension: 5}
    lengths = segment_lengths(patterns)
    assert route_length(patterns, lengths) == 3.0 + 4.0
