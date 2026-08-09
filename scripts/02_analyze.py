#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = ["duckdb"]
# ///
"""Analyze one-seat-ride / deinterlining share for trips crossing a subway junction.

Generalized so the same script can be re-run for other day types, other
station criteria, other data extracts, and other deinterlining scenarios
(different junction, different trunk-line pairs) just by passing flags.

Default scenario (the one this was built for): weekday trips on B/D/N/Q
originating south of Atlantic Av-Barclays Ctr in Brooklyn, heading toward
Manhattan through the DeKalb Ave interlining junction.

Examples:
    # Default DeKalb scenario
    uv run scripts/02_analyze.py

    # Same scenario, Saturdays instead of weekdays
    uv run scripts/02_analyze.py --day-type saturday

    # Same scenario, against a newer data extract
    uv run scripts/02_analyze.py --parquet data/mta_od_2025.parquet

    # A different junction/trunk pair, e.g. hypothetically Rogers Jct area
    uv run scripts/02_analyze.py --boundary-complex-id <id> --routes 2,3,4,5 \\
        --origin-borough Bk --trunk-a 4,5 --trunk-a-label "Lexington Av express" \\
        --trunk-b 2,3 --trunk-b-label "7 Av express"
"""

import argparse
import csv
import math
import pathlib

import duckdb

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
DAY_TYPE_PRESETS = {
    "weekday": WEEKDAYS,
    "saturday": ("Saturday",),
    "sunday": ("Sunday",),
    "all": None,
}


class Station:
    __slots__ = ("complex_id", "name", "borough", "routes", "lat", "lon")

    def __init__(self, complex_id: int, name: str, borough: str, routes: set[str], lat: float, lon: float):
        self.complex_id = complex_id
        self.name = name
        self.borough = borough
        self.routes = routes
        self.lat = lat
        self.lon = lon


def load_stations(path: pathlib.Path) -> dict[int, Station]:
    stations: dict[int, Station] = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            cid = int(row["complex_id"])
            stations[cid] = Station(
                complex_id=cid,
                name=row["display_name"],
                borough=row["borough"],
                routes=set(row["daytime_routes"].split()),
                lat=float(row["latitude"]),
                lon=float(row["longitude"]),
            )
    return stations


def load_individual_stations(path: pathlib.Path) -> list[Station]:
    """Per-physical-station rows (not complex centroids). A complex can merge
    several physical stations (e.g. Times Sq-42 St/Port Authority Bus
    Terminal), so its centroid can sit well away from any actual platform;
    these per-station points give accurate nearest-station distances."""
    out = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            out.append(
                Station(
                    complex_id=int(row["complex_id"]),
                    name=row["stop_name"],
                    borough=row["borough"],
                    routes=set(row["daytime_routes"].split()),
                    lat=float(row["gtfs_latitude"]),
                    lon=float(row["gtfs_longitude"]),
                )
            )
    return out


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def parse_route_set(s: str) -> set[str]:
    return {r.strip() for r in s.split(",") if r.strip()}


def classify_one_seat(origin_routes: set[str], dest_routes: set[str], routes: set[str], primary_routes: set[str]) -> tuple[bool, set[str]]:
    """A trip is one-seat if some shared route actually crosses the boundary
    junction (a primary route), or if the destination isn't served by any
    primary route anyway (so the non-primary connection, e.g. R, isn't
    standing in for a junction crossing that never really happens)."""
    shared = origin_routes & dest_routes & routes
    is_one_seat = bool(shared) and (bool(shared & primary_routes) or not (dest_routes & primary_routes))
    return is_one_seat, shared


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--parquet", type=pathlib.Path, default=DATA / "mta_od.parquet")
    parser.add_argument("--stations", type=pathlib.Path, default=DATA / "stations_complexes.csv")
    parser.add_argument(
        "--stations-individual",
        type=pathlib.Path,
        default=DATA / "stations_individual.csv",
        help="Per-physical-station reference CSV, used for accurate nearest-other-trunk distances",
    )

    parser.add_argument("--day-type", choices=sorted(DAY_TYPE_PRESETS), default="weekday")
    parser.add_argument("--days", help="Comma-separated exact 'Day of Week' values, overrides --day-type")

    parser.add_argument("--boundary-complex-id", type=int, default=617, help="Junction station (default: Atlantic Av-Barclays Ctr)")
    parser.add_argument("--origin-borough", default="Bk")
    parser.add_argument("--origin-side", choices=["south", "north"], default="south", help="Origin relative to boundary latitude")
    parser.add_argument("--dest-side", choices=["south", "north", "either"], default="north", help="Destination relative to boundary latitude (scopes to trips that actually cross the junction)")
    parser.add_argument(
        "--exclude-boundary-dest",
        action="store_true",
        help="Exclude the boundary complex itself from valid destinations (default: included, since ending at the junction still means the trip crossed it)",
    )
    parser.add_argument("--routes", default="B,D,N,Q", help="Route universe: origin filter + one-seat eligibility")
    parser.add_argument(
        "--primary-routes",
        default=None,
        help=(
            "Routes that actually cross the boundary junction (default: same as --routes). "
            "A route in --routes but not here (e.g. R, which reaches Manhattan via the Montague St "
            "Tunnel and never passes DeKalb/Atlantic) only counts a trip as one-seat if the shared "
            "route is a primary one, or if the destination isn't served by any primary route either "
            "-- otherwise it's treated as requiring a transfer at the junction, matching real rider "
            "behavior even though the OD data itself has no transfer field."
        ),
    )

    parser.add_argument("--trunk-a", default="B,D", help="Routes on trunk A")
    parser.add_argument("--trunk-a-label", default="6 Ave express")
    parser.add_argument("--trunk-b", default="N,Q", help="Routes on trunk B")
    parser.add_argument("--trunk-b-label", default="Broadway express")
    parser.add_argument("--close-threshold-m", type=float, default=300.0)

    parser.add_argument("--csv-out", type=pathlib.Path, help="Optional: dump classified per-OD-pair rows here")
    args = parser.parse_args()

    days = [d.strip() for d in args.days.split(",")] if args.days else DAY_TYPE_PRESETS[args.day_type]
    routes = parse_route_set(args.routes)
    primary_routes = parse_route_set(args.primary_routes) if args.primary_routes else routes
    trunk_a = parse_route_set(args.trunk_a)
    trunk_b = parse_route_set(args.trunk_b)

    stations = load_stations(args.stations)
    boundary_lat = stations[args.boundary_complex_id].lat
    print(f"Boundary: {stations[args.boundary_complex_id].name} (id {args.boundary_complex_id}), lat {boundary_lat:.6f}")
    print(f"Day filter: {days if days else 'all days'}")
    print(f"Route universe: {sorted(routes)}")

    def side_ok(lat: float, side: str) -> bool:
        if side == "either":
            return True
        return lat < boundary_lat if side == "south" else lat > boundary_lat

    origin_ids = [
        s.complex_id
        for s in stations.values()
        if s.borough == args.origin_borough and (s.routes & routes) and side_ok(s.lat, args.origin_side)
    ]
    origin_ids.sort()
    print(f"\nOrigin stations ({len(origin_ids)}):")
    for cid in origin_ids:
        s = stations[cid]
        print(f"  {cid:>4}  {s.name}  routes={sorted(s.routes)}")

    con = duckdb.connect()
    day_filter_sql = "TRUE" if not days else "\"Day of Week\" IN (" + ", ".join(f"'{d}'" for d in days) + ")"
    origin_filter_sql = "\"Origin Station Complex ID\" IN (" + ", ".join(str(i) for i in origin_ids) + ")"

    n_days_query = f"""
        SELECT COUNT(DISTINCT CAST(Timestamp AS DATE))
        FROM '{args.parquet}'
        WHERE {day_filter_sql}
    """
    (n_distinct_days,) = con.execute(n_days_query).fetchone()

    # "riders" throughout is average weekday (or whichever day-type) ridership,
    # i.e. the sum over all matching days divided by the number of distinct
    # matching days -- not a multi-day total.
    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM '{args.parquet}'
        WHERE {day_filter_sql} AND {origin_filter_sql}
        GROUP BY 1, 2
    """
    pairs = con.execute(pairs_query).fetchall()
    print(f"\n{len(pairs):,} distinct origin/destination pairs, averaged over {n_distinct_days} distinct days matching the day filter")

    # Scope to trips that actually cross the boundary (dest on the far side,
    # or at the boundary complex itself unless excluded).
    scoped = []
    for origin_id, dest_id, riders in pairs:
        dest = stations.get(dest_id)
        if dest is None:
            continue
        at_boundary = dest_id == args.boundary_complex_id and not args.exclude_boundary_dest
        if not at_boundary and not side_ok(dest.lat, args.dest_side):
            continue
        scoped.append((origin_id, dest_id, riders))

    total_riders = sum(r for _, _, r in scoped)
    one_seat_riders = 0.0
    classified_one_seat_riders = 0.0
    close_riders = 0.0

    individual_stations = load_individual_stations(args.stations_individual)
    points_by_complex: dict[int, list[tuple[float, float]]] = {}
    for s in individual_stations:
        points_by_complex.setdefault(s.complex_id, []).append((s.lat, s.lon))

    def dest_points(dest: Station) -> list[tuple[float, float]]:
        return points_by_complex.get(dest.complex_id, [(dest.lat, dest.lon)])

    # Candidate points for the nearest-other-trunk search, system-wide (not
    # restricted to any borough): straight-line distance is already the
    # approximation this whole script uses for "close" everywhere else, so
    # there's no reason to special-case borough boundaries here too.
    trunk_a_points = [(s.lat, s.lon) for s in individual_stations if s.routes & trunk_a]
    trunk_b_points = [(s.lat, s.lon) for s in individual_stations if s.routes & trunk_b]

    def min_dist_to_points(points: list[tuple[float, float]], candidates: list[tuple[float, float]]) -> float | None:
        if not candidates:
            return None
        return min(haversine_m(lat, lon, clat, clon) for lat, lon in points for clat, clon in candidates)

    rows_out = []
    for origin_id, dest_id, riders in scoped:
        origin = stations[origin_id]
        dest = stations.get(dest_id)
        dest_routes = dest.routes if dest else set()
        is_one_seat, shared = classify_one_seat(origin.routes, dest_routes, routes, primary_routes)
        if is_one_seat:
            one_seat_riders += riders

        close = None
        dist_m = None
        if is_one_seat and dest:
            if not (shared & primary_routes):
                # This one-seat connection doesn't use any route that
                # actually crosses the boundary junction (e.g. it's via R,
                # which reaches Manhattan through the Montague St Tunnel and
                # never goes near DeKalb/Atlantic). Deinterlining the
                # junction can't affect a trip that never uses it, so this
                # rider needs no extra walk/transfer either way -- trivially
                # close.
                close, dist_m = True, 0.0
            else:
                # Trunk membership is a property of the destination complex
                # itself (what it's near/at), not of which specific shared
                # route made this particular pair one-seat.
                home_a = bool(dest_routes & trunk_a)
                home_b = bool(dest_routes & trunk_b)
                if home_a and home_b:
                    # The destination already has routes from both groups
                    # (e.g. a junction complex like Atlantic Av-Barclays Ctr
                    # or DeKalb Av) -- trivially "at" the other trunk.
                    close, dist_m = True, 0.0
                elif home_a:
                    dist_m = min_dist_to_points(dest_points(dest), trunk_b_points)
                    close = None if dist_m is None else dist_m <= args.close_threshold_m
                elif home_b:
                    dist_m = min_dist_to_points(dest_points(dest), trunk_a_points)
                    close = None if dist_m is None else dist_m <= args.close_threshold_m
                # close/dist_m stay None only if the destination has neither
                # trunk's routes at all -- no "other trunk" to speak of.

            if close is not None:
                classified_one_seat_riders += riders
                if close:
                    close_riders += riders

        if args.csv_out:
            rows_out.append(
                {
                    "origin_id": origin_id,
                    "origin_name": origin.name,
                    "dest_id": dest_id,
                    "dest_name": dest.name if dest else "",
                    "riders": riders,
                    "one_seat": is_one_seat,
                    "dest_borough": dest.borough if dest else "",
                    "close_to_other_trunk": close,
                    "dist_to_other_trunk_m": dist_m,
                }
            )

    print(f"\n=== Scope: origin in {{south of boundary}}, destination {args.dest_side} of boundary, day-type={args.day_type} ===")
    print(f"Average {args.day_type} ridership (based on {n_distinct_days} distinct days in the data): {total_riders:,.0f}")
    if total_riders:
        print(f"One-seat (no transfer): {one_seat_riders:,.0f} ({100 * one_seat_riders / total_riders:.1f}%)")
        print(f"Transfer required:      {total_riders - one_seat_riders:,.0f} ({100 * (1 - one_seat_riders / total_riders):.1f}%)")

    print(f"\n=== Of one-seat rides, destinations with a {args.trunk_a_label}/{args.trunk_b_label} classification ===")
    print(f"One-seat riders with a trunk classification: {classified_one_seat_riders:,.0f}")
    if classified_one_seat_riders:
        pct = 100 * close_riders / classified_one_seat_riders
        print(
            f"...within {args.close_threshold_m:.0f}m of the other trunk "
            f"({args.trunk_a_label} vs {args.trunk_b_label}): {close_riders:,.0f} ({pct:.1f}%)"
        )

    print("\n=== Per-origin-station breakdown (avg weekday riders) ===")
    per_origin: dict[int, list[float]] = {cid: [0.0, 0.0] for cid in origin_ids}
    per_dest: dict[int, list[float]] = {}
    for origin_id, dest_id, riders in scoped:
        origin = stations[origin_id]
        dest = stations.get(dest_id)
        dest_routes = dest.routes if dest else set()
        is_one_seat, _ = classify_one_seat(origin.routes, dest_routes, routes, primary_routes)
        per_origin[origin_id][0] += riders
        if is_one_seat:
            per_origin[origin_id][1] += riders
        entry = per_dest.setdefault(dest_id, [0.0, 0.0])
        entry[0] += riders
        if is_one_seat:
            entry[1] += riders
    for cid in origin_ids:
        total, one_seat = per_origin[cid]
        pct = 100 * one_seat / total if total else float("nan")
        print(f"  {stations[cid].name:<45} total={total:>9,.0f}  one-seat={pct:5.1f}%")

    print("\n=== Per-destination-station breakdown (avg weekday riders, sorted by total) ===")
    for dest_id, (total, one_seat) in sorted(per_dest.items(), key=lambda kv: kv[1][0], reverse=True):
        dest = stations.get(dest_id)
        name = dest.name if dest else f"complex {dest_id}"
        pct = 100 * one_seat / total if total else float("nan")
        print(f"  {name:<55} total={total:>9,.0f}  one-seat={pct:5.1f}%")

    if args.csv_out:
        with args.csv_out.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()) if rows_out else [])
            writer.writeheader()
            writer.writerows(rows_out)
        print(f"\nWrote {len(rows_out):,} rows to {args.csv_out}")


if __name__ == "__main__":
    main()
