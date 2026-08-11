#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = ["duckdb", "typer"]
# ///
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import duckdb
import typer

app = typer.Typer(rich_markup_mode=None, add_completion=False)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
DAY_TYPE_PRESETS = {
    "weekday": WEEKDAYS,
    "saturday": ("Saturday",),
    "sunday": ("Sunday",),
    "all": None,
}


@dataclass(slots=True)
class Station:
    complex_id: int
    name: str
    borough: str
    routes: set[str]
    lat: float
    lon: float


def load_stations(path: Path) -> dict[int, Station]:
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


def load_individual_stations(path: Path) -> list[Station]:
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
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * r * math.asin(math.sqrt(a))


def parse_route_set(s: str) -> set[str]:
    return {r.strip() for r in s.split(",") if r.strip()}


def classify_one_seat(
    origin_routes: set[str],
    dest_routes: set[str],
    routes: set[str],
    primary_routes: set[str],
) -> tuple[bool, set[str]]:
    """A trip is one-seat if some shared route actually crosses the boundary
    junction (a primary route), or if the destination isn't served by any
    primary route anyway (so the non-primary connection, e.g. R, isn't
    standing in for a junction crossing that never really happens)."""
    shared = origin_routes & dest_routes & routes
    is_one_seat = bool(shared) and (
        bool(shared & primary_routes) or not (dest_routes & primary_routes)
    )
    return is_one_seat, shared


@app.command()
def main(
    parquet: Annotated[Path, typer.Option()] = DATA / "mta_od.parquet",
    stations: Annotated[Path, typer.Option()] = DATA / "stations_complexes.csv",
    stations_individual: Annotated[
        Path,
        typer.Option(
            help=(
                "Per-physical-station reference CSV, used for accurate "
                "nearest-other-trunk distances"
            ),
        ),
    ] = DATA / "stations_individual.csv",
    day_type: Annotated[
        str, typer.Option(help="One of: " + ", ".join(sorted(DAY_TYPE_PRESETS)))
    ] = "weekday",
    days: Annotated[
        str | None,
        typer.Option(
            help="Comma-separated exact 'Day of Week' values, overrides --day-type"
        ),
    ] = None,
    boundary_complex_id: Annotated[
        int, typer.Option(help="Junction station (default: Atlantic Av-Barclays Ctr)")
    ] = 617,
    origin_borough: Annotated[str, typer.Option()] = "Bk",
    origin_side: Annotated[
        str,
        typer.Option(help="One of: south, north. Origin relative to boundary latitude"),
    ] = "south",
    dest_side: Annotated[
        str,
        typer.Option(
            help=(
                "One of: south, north, either. Destination relative to boundary "
                "latitude (scopes to trips that actually cross the junction)"
            )
        ),
    ] = "north",
    exclude_boundary_dest: Annotated[
        bool,
        typer.Option(
            help=(
                "Exclude the boundary complex itself from valid destinations "
                "(default: included, since ending at the junction still means "
                "the trip crossed it)"
            )
        ),
    ] = False,
    routes: Annotated[
        str, typer.Option(help="Route universe: origin filter + one-seat eligibility")
    ] = "B,D,N,Q",
    primary_routes: Annotated[
        str | None,
        typer.Option(
            help=(
                "Routes that actually cross the boundary junction (default: same as "
                "--routes). A route in --routes but not here (e.g. R, which reaches "
                "Manhattan via the Montague St Tunnel and never passes "
                "DeKalb/Atlantic) "
                "only counts a trip as one-seat if the shared route is a primary one, "
                "or if the destination isn't served by any primary route either -- "
                "otherwise it's treated as requiring a transfer at the junction, "
                "matching real rider behavior even though the OD data itself has no "
                "transfer field."
            ),
        ),
    ] = None,
    trunk_a: Annotated[str, typer.Option(help="Routes on trunk A")] = "B,D",
    trunk_a_label: Annotated[str, typer.Option()] = "6 Ave express",
    trunk_b: Annotated[str, typer.Option(help="Routes on trunk B")] = "N,Q",
    trunk_b_label: Annotated[str, typer.Option()] = "Broadway express",
    close_threshold_m: Annotated[float, typer.Option()] = 300.0,
    csv_out: Annotated[
        Path | None,
        typer.Option(help="Optional: dump classified per-OD-pair rows here"),
    ] = None,
) -> None:
    """Analyze one-seat-ride / deinterlining share for trips crossing a subway junction.

    Generalized so the same script can be re-run for other day types, other
    station criteria, other data extracts, and other deinterlining scenarios
    (different junction, different trunk-line pairs) just by passing flags.

    Default scenario (the one this was built for): weekday trips on B/D/N/Q
    originating south of Atlantic Av-Barclays Ctr in Brooklyn, heading toward
    Manhattan through the DeKalb Ave interlining junction.

    \b
    Examples:
        # Default DeKalb scenario
        uv run scripts/02_analyze.py

    \b
        # Same scenario, Saturdays instead of weekdays
        uv run scripts/02_analyze.py --day-type saturday

    \b
        # Same scenario, against a newer data extract
        uv run scripts/02_analyze.py --parquet data/mta_od_2025.parquet

    \b
        # A different junction/trunk pair, e.g. hypothetically Rogers Jct area
        uv run scripts/02_analyze.py --boundary-complex-id <id> --routes 2,3,4,5 \\
            --origin-borough Bk --trunk-a 4,5 --trunk-a-label "Lexington Av express" \\
            --trunk-b 2,3 --trunk-b-label "7 Av express"
    """
    if day_type not in DAY_TYPE_PRESETS:
        raise typer.BadParameter(
            f"--day-type must be one of {sorted(DAY_TYPE_PRESETS)}, got {day_type!r}"
        )
    if origin_side not in ("south", "north"):
        raise typer.BadParameter(
            f"--origin-side must be one of ['south', 'north'], got {origin_side!r}"
        )
    if dest_side not in ("south", "north", "either"):
        raise typer.BadParameter(
            "--dest-side must be one of ['south', 'north', 'either'], "
            f"got {dest_side!r}"
        )

    days_list = (
        [d.strip() for d in days.split(",")] if days else DAY_TYPE_PRESETS[day_type]
    )
    routes_set = parse_route_set(routes)
    primary_routes_set = (
        parse_route_set(primary_routes) if primary_routes else routes_set
    )
    trunk_a_set = parse_route_set(trunk_a)
    trunk_b_set = parse_route_set(trunk_b)

    stations_by_id = load_stations(stations)
    boundary_lat = stations_by_id[boundary_complex_id].lat
    print(
        f"Boundary: {stations_by_id[boundary_complex_id].name} "
        f"(id {boundary_complex_id}), lat {boundary_lat:.6f}"
    )
    print(f"Day filter: {days_list if days_list else 'all days'}")
    print(f"Route universe: {sorted(routes_set)}")

    def side_ok(lat: float, side: str) -> bool:
        if side == "either":
            return True
        return lat < boundary_lat if side == "south" else lat > boundary_lat

    origin_ids = [
        s.complex_id
        for s in stations_by_id.values()
        if s.borough == origin_borough
        and (s.routes & routes_set)
        and side_ok(s.lat, origin_side)
    ]
    origin_ids.sort()
    print(f"\nOrigin stations ({len(origin_ids)}):")
    for cid in origin_ids:
        s = stations_by_id[cid]
        print(f"  {cid:>4}  {s.name}  routes={sorted(s.routes)}")

    con = duckdb.connect()
    day_filter_sql = (
        "TRUE"
        if not days_list
        else '"Day of Week" IN (' + ", ".join(f"'{d}'" for d in days_list) + ")"
    )
    origin_filter_sql = (
        '"Origin Station Complex ID" IN (' + ", ".join(str(i) for i in origin_ids) + ")"
    )

    n_days_query = f"""
        SELECT COUNT(DISTINCT CAST(Timestamp AS DATE))
        FROM '{parquet}'
        WHERE {day_filter_sql}
    """
    result = con.execute(n_days_query).fetchone()
    assert result is not None, "aggregate query always returns exactly one row"
    (n_distinct_days,) = result

    # "riders" throughout is average weekday (or whichever day-type) ridership,
    # i.e. the sum over all matching days divided by the number of distinct
    # matching days -- not a multi-day total.
    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM '{parquet}'
        WHERE {day_filter_sql} AND {origin_filter_sql}
        GROUP BY 1, 2
    """
    pairs = con.execute(pairs_query).fetchall()
    print(
        f"\n{len(pairs):,} distinct origin/destination pairs, averaged over "
        f"{n_distinct_days} distinct days matching the day filter"
    )

    # Scope to trips that actually cross the boundary (dest on the far side,
    # or at the boundary complex itself unless excluded).
    scoped = []
    for origin_id, dest_id, riders in pairs:
        dest = stations_by_id.get(dest_id)
        if dest is None:
            continue
        at_boundary = dest_id == boundary_complex_id and not exclude_boundary_dest
        if not at_boundary and not side_ok(dest.lat, dest_side):
            continue
        scoped.append((origin_id, dest_id, riders))

    total_riders = sum(r for _, _, r in scoped)
    one_seat_riders = 0.0
    classified_one_seat_riders = 0.0
    close_riders = 0.0

    individual_stations = load_individual_stations(stations_individual)
    points_by_complex: dict[int, list[tuple[float, float]]] = {}
    for s in individual_stations:
        points_by_complex.setdefault(s.complex_id, []).append((s.lat, s.lon))

    def dest_points(dest: Station) -> list[tuple[float, float]]:
        return points_by_complex.get(dest.complex_id, [(dest.lat, dest.lon)])

    # Candidate points for the nearest-other-trunk search, system-wide (not
    # restricted to any borough): straight-line distance is already the
    # approximation this whole script uses for "close" everywhere else, so
    # there's no reason to special-case borough boundaries here too.
    trunk_a_points = [
        (s.lat, s.lon) for s in individual_stations if s.routes & trunk_a_set
    ]
    trunk_b_points = [
        (s.lat, s.lon) for s in individual_stations if s.routes & trunk_b_set
    ]

    def min_dist_to_points(
        points: list[tuple[float, float]], candidates: list[tuple[float, float]]
    ) -> float | None:
        if not candidates:
            return None
        return min(
            haversine_m(lat, lon, clat, clon)
            for lat, lon in points
            for clat, clon in candidates
        )

    rows_out = []
    for origin_id, dest_id, riders in scoped:
        origin = stations_by_id[origin_id]
        dest = stations_by_id.get(dest_id)
        dest_routes = dest.routes if dest else set()
        is_one_seat, shared = classify_one_seat(
            origin.routes, dest_routes, routes_set, primary_routes_set
        )
        if is_one_seat:
            one_seat_riders += riders

        close = None
        dist_m = None
        if is_one_seat and dest:
            if not (shared & primary_routes_set):
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
                home_a = bool(dest_routes & trunk_a_set)
                home_b = bool(dest_routes & trunk_b_set)
                if home_a and home_b:
                    # The destination already has routes from both groups
                    # (e.g. a junction complex like Atlantic Av-Barclays Ctr
                    # or DeKalb Av) -- trivially "at" the other trunk.
                    close, dist_m = True, 0.0
                elif home_a:
                    dist_m = min_dist_to_points(dest_points(dest), trunk_b_points)
                    close = None if dist_m is None else dist_m <= close_threshold_m
                elif home_b:
                    dist_m = min_dist_to_points(dest_points(dest), trunk_a_points)
                    close = None if dist_m is None else dist_m <= close_threshold_m
                # close/dist_m stay None only if the destination has neither
                # trunk's routes at all -- no "other trunk" to speak of.

            if close is not None:
                classified_one_seat_riders += riders
                if close:
                    close_riders += riders

        if csv_out:
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

    print(
        f"\n=== Scope: origin in {{south of boundary}}, destination "
        f"{dest_side} of boundary, day-type={day_type} ==="
    )
    print(
        f"Average {day_type} ridership (based on {n_distinct_days} "
        f"distinct days in the data): {total_riders:,.0f}"
    )
    if total_riders:
        print(
            f"One-seat (no transfer): {one_seat_riders:,.0f} "
            f"({100 * one_seat_riders / total_riders:.1f}%)"
        )
        print(
            f"Transfer required:      {total_riders - one_seat_riders:,.0f} "
            f"({100 * (1 - one_seat_riders / total_riders):.1f}%)"
        )

    print(
        f"\n=== Of one-seat rides, destinations with a "
        f"{trunk_a_label}/{trunk_b_label} classification ==="
    )
    print(
        "One-seat riders with a trunk classification: "
        f"{classified_one_seat_riders:,.0f}"
    )
    if classified_one_seat_riders:
        pct = 100 * close_riders / classified_one_seat_riders
        print(
            f"...within {close_threshold_m:.0f}m of the other trunk "
            f"({trunk_a_label} vs {trunk_b_label}): "
            f"{close_riders:,.0f} ({pct:.1f}%)"
        )

    print("\n=== Per-origin-station breakdown (avg weekday riders) ===")
    per_origin: dict[int, list[float]] = {cid: [0.0, 0.0] for cid in origin_ids}
    per_dest: dict[int, list[float]] = {}
    for origin_id, dest_id, riders in scoped:
        origin = stations_by_id[origin_id]
        dest = stations_by_id.get(dest_id)
        dest_routes = dest.routes if dest else set()
        is_one_seat, _ = classify_one_seat(
            origin.routes, dest_routes, routes_set, primary_routes_set
        )
        per_origin[origin_id][0] += riders
        if is_one_seat:
            per_origin[origin_id][1] += riders
        entry = per_dest.setdefault(dest_id, [0.0, 0.0])
        entry[0] += riders
        if is_one_seat:
            entry[1] += riders
    for cid in origin_ids:
        name = stations_by_id[cid].name
        total, one_seat = per_origin[cid]
        pct = 100 * one_seat / total if total else float("nan")
        print(f"  {name:<45} total={total:>9,.0f}  one-seat={pct:5.1f}%")

    print(
        "\n=== Per-destination-station breakdown "
        "(avg weekday riders, sorted by total) ==="
    )
    for dest_id, (total, one_seat) in sorted(
        per_dest.items(), key=lambda kv: kv[1][0], reverse=True
    ):
        dest = stations_by_id.get(dest_id)
        name = dest.name if dest else f"complex {dest_id}"
        pct = 100 * one_seat / total if total else float("nan")
        print(f"  {name:<55} total={total:>9,.0f}  one-seat={pct:5.1f}%")

    if csv_out:
        with csv_out.open("w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=list(rows_out[0].keys()) if rows_out else []
            )
            writer.writeheader()
            writer.writerows(rows_out)
        print(f"\nWrote {len(rows_out):,} rows to {csv_out}")


if __name__ == "__main__":
    app()
