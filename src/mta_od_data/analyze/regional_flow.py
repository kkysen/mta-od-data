import csv
import shlex
import sys
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Annotated

import duckdb
from typer import Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import DAY_TYPE_PRESETS, DayType, Station
from mta_od_data.analyze.regions import (
    Region,
    RegionPreset,
    bbox_region,
    borough_region,
    parse_bbox,
    region_from_preset,
)

app = Typer()


@dataclass(slots=True)
class FlowRow:
    origin_id: int
    origin_name: str
    dest_id: int
    dest_name: str
    riders: float
    origin_in: bool
    dest_in: bool

    @property
    def flow(self) -> str:
        return f"{'in' if self.origin_in else 'out'}→{'in' if self.dest_in else 'out'}"


@dataclass(slots=True)
class RegionalFlowResult:
    region_name: str
    total_riders: float
    in_in: float
    in_out: float
    out_in: float
    out_out: float
    rows: list[FlowRow]

    @property
    def inter(self) -> float:
        """Interregional: riders whose trip crosses the region boundary,
        either direction."""
        return self.in_out + self.out_in

    @property
    def intra(self) -> float:
        """Intraregional: riders whose trip never crosses the region
        boundary, on either side of it -- the complement of `inter`."""
        return self.in_in + self.out_out

    def pct(self, riders: float) -> float:
        return 100 * riders / self.total_riders if self.total_riders else float("nan")

    def print_headline(self, *, day_type: DayType) -> None:
        print(f"\n=== Regional flow: {self.region_name} ===")
        print(f"Average {day_type} ridership: {self.total_riders:,.0f}")
        print(
            f"Outside -> Inside  (entering the region):   "
            f"{self.out_in:>12,.0f} ({self.pct(self.out_in):5.1f}%)"
        )
        print(
            f"Inside  -> Outside (leaving the region):    "
            f"{self.in_out:>12,.0f} ({self.pct(self.in_out):5.1f}%)"
        )
        print(
            f"Inside  -> Inside  (internal to the region): "
            f"{self.in_in:>12,.0f} ({self.pct(self.in_in):5.1f}%)"
        )
        print(
            f"Outside -> Outside (never touches the region): "
            f"{self.out_out:>12,.0f} ({self.pct(self.out_out):5.1f}%)"
        )
        print(
            f"  Inter (crosses the boundary, either direction): "
            f"{self.inter:>12,.0f} ({self.pct(self.inter):5.1f}%)"
        )
        print(
            f"  Intra (same side throughout, either side):      "
            f"{self.intra:>12,.0f} ({self.pct(self.intra):5.1f}%)"
        )

    def render_markdown(
        self, *, day_type: DayType, top_n: int, csv_out: Path | None
    ) -> str:
        lines: list[str] = []
        lines.append("## Headline numbers")
        lines.append("")
        lines.append(f"Total: {self.total_riders:,.0f} riders/{day_type}")
        lines.append("")
        lines.append("| Flow | Riders | % Total |")
        lines.append("| --- | --- | --- |")
        lines.append(
            f"| Outside -> Inside | {self.out_in:,.0f} | {self.pct(self.out_in):.1f}% |"
        )
        lines.append(
            f"| Inside -> Outside | {self.in_out:,.0f} | {self.pct(self.in_out):.1f}% |"
        )
        lines.append(
            f"| Inside -> Inside | {self.in_in:,.0f} | {self.pct(self.in_in):.1f}% |"
        )
        lines.append(
            f"| Outside -> Outside | {self.out_out:,.0f} | "
            f"{self.pct(self.out_out):.1f}% |"
        )
        lines.append(f"| **Inter** | {self.inter:,.0f} | {self.pct(self.inter):.1f}% |")
        lines.append(f"| **Intra** | {self.intra:,.0f} | {self.pct(self.intra):.1f}% |")
        lines.append("")

        lines.append(f"## Top {top_n} origin/destination pairs")
        lines.append("")
        lines.append("| # | Riders | % Total | Flow | Origin -> Destination |")
        lines.append("| --- | --- | --- | --- | --- |")

        def pair_riders(r: FlowRow) -> float:
            return r.riders

        top_pairs = sorted(self.rows, key=pair_riders, reverse=True)[:top_n]
        for i, r in enumerate(top_pairs, start=1):
            lines.append(
                f"| {i} | {r.riders:,.0f} | {self.pct(r.riders):.2f}% | {r.flow} | "
                f"{r.origin_name} → {r.dest_name} |"
            )
        lines.append("")

        if csv_out:
            lines.append(
                f"_Full row-level detail (every origin/destination pair, not just "
                f"the top {top_n}): `{csv_out}`._"
            )
            lines.append("")
        return "\n".join(lines)


def resolve_region(
    *,
    preset: RegionPreset,
    region_borough: str | None,
    region_bbox: str | None,
    region_label: str | None,
    valid_boroughs: set[str],
) -> Region:
    if region_borough is not None and region_bbox is not None:
        print(
            "error: --region-borough and --region-bbox can't be combined",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if region_borough is not None:
        boroughs = {b.strip() for b in region_borough.split(",") if b.strip()}
        unknown = boroughs - valid_boroughs
        if unknown:
            print(
                f"error: --region-borough has unknown code(s) {sorted(unknown)} -- "
                f"valid codes are {sorted(valid_boroughs)}",
                file=sys.stderr,
            )
            raise SystemExit(1)
        label = (
            region_label or f"custom region (boroughs: {','.join(sorted(boroughs))})"
        )
        return borough_region(label, boroughs)
    if region_bbox is not None:
        try:
            bbox = parse_bbox(region_bbox)
        except ValueError as e:
            print(f"error: --region-bbox {e}", file=sys.stderr)
            raise SystemExit(1) from e
        label = region_label or f"custom region (bbox {region_bbox})"
        return bbox_region(label, bbox)
    return region_from_preset(preset)


def write_csv(path: Path, rows: list[FlowRow]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[fld.name for fld in fields(FlowRow)])
        writer.writeheader()
        writer.writerows(asdict(r) for r in rows)
    print(f"\nWrote {len(rows):,} rows to {path}")


@app.command(name="regional-flow")
def regional_flow(
    parquet: Annotated[Path, Option()] = DATA / "mta_od.parquet",
    stations: Annotated[Path, Option()] = DATA / "stations_complexes.csv",
    day_type: Annotated[DayType, Option()] = DayType.WEEKDAY,
    days: Annotated[
        str | None,
        Option(help="Comma-separated exact 'Day of Week' values, overrides --day-type"),
    ] = None,
    region: Annotated[
        RegionPreset, Option(help="Named region preset")
    ] = RegionPreset.CBD,
    region_borough: Annotated[
        str | None,
        Option(
            help=(
                "Custom region: comma-separated borough codes (M, Bk, Bx, Q, SI), "
                "e.g. 'M,Bk'. Overrides --region."
            )
        ),
    ] = None,
    region_bbox: Annotated[
        str | None,
        Option(
            help=(
                "Custom region: MIN_LAT,MIN_LON,MAX_LAT,MAX_LON bounding box. "
                "Overrides --region."
            )
        ),
    ] = None,
    region_label: Annotated[
        str | None,
        Option(
            help=(
                "Display name for a custom region (--region-borough/"
                "--region-bbox); ignored for a --region preset"
            )
        ),
    ] = None,
    csv_out: Annotated[
        Path | None,
        Option(help="Optional: dump classified per-OD-pair rows here"),
    ] = None,
    markdown_out: Annotated[
        Path | None,
        Option(help="Optional: write a markdown report here"),
    ] = None,
    top_n: Annotated[
        int, Option(help="Row count for the markdown top-pairs table")
    ] = 25,
) -> None:
    """Analyze how ridership flows across a region's boundary: what share of
    riders go from outside the region into it, from inside out, stay inside
    it, or never touch it at all.

    Unlike `one-seat-rides`, this is system-wide (no route filter, no side
    of a single junction) -- every origin/destination pair in the data is
    classified by whether each end falls inside the given region.

    \b
    Examples:
        # Default: Lower Manhattan (below 60th St / Congestion Relief Zone)
        mta-od-data analyze regional-flow

    \b
        # A whole borough instead
        mta-od-data analyze regional-flow --region brooklyn

    \b
        # A custom region: two boroughs at once
        mta-od-data analyze regional-flow --region-borough M,Bk \\
            --region-label "Manhattan + Brooklyn"

    \b
        # A custom lat/lon bounding box (e.g. roughly Midtown Manhattan)
        mta-od-data analyze regional-flow \\
            --region-bbox 40.744,-74.005,40.771,-73.968 \\
            --region-label "Midtown Manhattan"
    """
    days_list = (
        [d.strip() for d in days.split(",")] if days else DAY_TYPE_PRESETS[day_type]
    )
    stations_by_id = Station.load_complexes(stations)
    valid_boroughs = {s.borough for s in stations_by_id.values()}
    region_def = resolve_region(
        preset=region,
        region_borough=region_borough,
        region_bbox=region_bbox,
        region_label=region_label,
        valid_boroughs=valid_boroughs,
    )

    n_inside = sum(1 for s in stations_by_id.values() if region_def.contains(s))
    if n_inside == 0:
        print(
            f"error: region {region_def.name!r} matches 0 of "
            f"{len(stations_by_id)} stations -- check "
            "--region/--region-borough/--region-bbox",
            file=sys.stderr,
        )
        raise SystemExit(1)
    print(f"Region: {region_def.name} ({n_inside} of {len(stations_by_id)} stations)")
    print(f"Day filter: {days_list if days_list else 'all days'}")

    con = duckdb.connect()
    day_params: list[str] = list(days_list) if days_list else []
    day_filter_sql = (
        "TRUE"
        if not days_list
        else '"Day of Week" IN (' + ", ".join("?" for _ in days_list) + ")"
    )

    n_days_query = f"""
        SELECT COUNT(DISTINCT CAST(Timestamp AS DATE))
        FROM read_parquet(?)
        WHERE {day_filter_sql}
    """
    n_days_result: tuple[int] | None = con.execute(
        n_days_query, [str(parquet), *day_params]
    ).fetchone()
    assert n_days_result is not None, "aggregate query always returns exactly one row"
    (n_distinct_days,) = n_days_result

    # "riders" throughout is average weekday (or whichever day-type) ridership,
    # i.e. the sum over all matching days divided by the number of distinct
    # matching days -- not a multi-day total. System-wide: no origin filter,
    # unlike `one-seat-rides`, since the question here is about every trip's
    # relationship to the region, not just trips from a pre-selected corridor.
    pairs_query = f"""
        SELECT "Origin Station Complex ID" AS origin_id,
               "Destination Station Complex ID" AS dest_id,
               SUM("Estimated Average Ridership") / {n_distinct_days} AS riders
        FROM read_parquet(?)
        WHERE {day_filter_sql}
        GROUP BY 1, 2
    """
    pairs: list[tuple[int, int, float]] = con.execute(
        pairs_query, [str(parquet), *day_params]
    ).fetchall()
    print(
        f"\n{len(pairs):,} distinct origin/destination pairs, averaged over "
        f"{n_distinct_days} distinct days matching the day filter"
    )

    rows: list[FlowRow] = []
    total_riders = 0.0
    in_in = in_out = out_in = out_out = 0.0
    for origin_id, dest_id, riders in pairs:
        origin = stations_by_id.get(origin_id)
        dest = stations_by_id.get(dest_id)
        if origin is None or dest is None:
            missing_id = origin_id if origin is None else dest_id
            print(
                f"error: station complex {missing_id} not found in "
                f"{stations} -- refetch station reference data with "
                "`mta-od-data prepare --force-stations`",
                file=sys.stderr,
            )
            raise SystemExit(1)

        origin_in = region_def.contains(origin)
        dest_in = region_def.contains(dest)
        total_riders += riders
        if origin_in and dest_in:
            in_in += riders
        elif origin_in and not dest_in:
            in_out += riders
        elif not origin_in and dest_in:
            out_in += riders
        else:
            out_out += riders

        # Bare names, not `display()` -- the route(s) a rider actually used
        # aren't knowable here the way `one_seat_rides` narrows them (there's
        # no route universe to narrow against), so showing a merged complex's
        # full route list would just be noise for a region-boundary question.
        rows.append(
            FlowRow(
                origin_id=origin_id,
                origin_name=origin.name,
                dest_id=dest_id,
                dest_name=dest.name,
                riders=riders,
                origin_in=origin_in,
                dest_in=dest_in,
            )
        )

    result = RegionalFlowResult(
        region_name=region_def.name,
        total_riders=total_riders,
        in_in=in_in,
        in_out=in_out,
        out_in=out_in,
        out_out=out_out,
        rows=rows,
    )
    result.print_headline(day_type=day_type)

    if csv_out:
        write_csv(csv_out, result.rows)

    if markdown_out:
        produced_by = shlex.join([Path(sys.argv[0]).name, *sys.argv[1:]])
        preamble_lines = [
            f"# Regional flow: {result.region_name}",
            "",
            f"Scenario: average {day_type} ridership ({n_distinct_days} distinct "
            f"days in the data), every origin/destination pair classified by "
            f"whether each end falls inside {result.region_name}.",
            "",
            f"Produced by `{produced_by}`.",
            "",
        ]
        sections = [
            "\n".join(preamble_lines),
            result.render_markdown(day_type=day_type, top_n=top_n, csv_out=csv_out),
        ]
        markdown_out.write_text("\n---\n\n".join(sections))
        print(f"\nWrote markdown report to {markdown_out}")
