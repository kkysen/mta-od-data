"""Average weekday ridership by station complex, station, station direction, route,
or line,
from `mta-od-data raptor assign-range`'s paths.

Each measure is a sum of paths' riders, so it's taken over
`average_path_riders`' average of each path over the manifest's dates,
once per way of counting riders (a column each):
as in the OD data, and scaled by each `--od-factors` file,
all with fare evaders unless `--no-fare-evasion`.

- A place (complex, station, station direction)
  counts each ride's boarding and alighting there,
  which of those are transfers (not the journey's first boarding or last alighting),
  and riders staying on a train stopping there.
  With `--route` but not `--by route`, consecutive rides on `--route`'s routes
  changing at the same stop are one ride: an N to R change at 59 St is neither.
- A route counts each journey riding it once, however many of its rides are on it.
  Routes with express variants (5X 6X 7X FX) count as the route, `5`,
  and again as their local, `5L`, or express, `5X`, alone.
- A line counts each journey with a ride on its track once:
  between two stops one after the other on it (`lines.json5`),
  as `raptor` paths list every stop a ride stops at.
"""

from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from csv import DictReader
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, Any

import json5
from typer import BadParameter, Context, Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import (
    Complex,
    MissingComplex,
    abbreviate_name,
    display_station,
)
from mta_od_data.analyze.markdown import table_row, table_rule
from mta_od_data.analyze.path_riders import read_manifest
from mta_od_data.invocation import produced_by
from mta_od_data.ridership.cache import cached_compute
from mta_od_data.ridership.charts import Chart, table_charts
from mta_od_data.ridership.compute import (
    CAR_FT,
    PLACES,
    By,
    Column,
    RouteService,
    base_route,
    load_train_lengths,
    period,
)
from mta_od_data.ridership.trips import Train

app = Typer()

HERE = Path(__file__).parent
DEFAULT_MANIFEST = DATA / "raptor" / "manifest.csv"
# Scaled to 2019's counted entries (`scale-od --to-counts`), before the pandemic.
# Not also to the OD data's own year's: its trips are within ~1% of 2025's counts
# systemwide, and 2% at 80% of stations, so that column barely differed.
DEFAULT_OD_FACTORS = [DATA / "mta_od_2019_counted.factors.parquet"]
DEFAULT_LINES = HERE / "lines.json5"
DIRECTION_LABELS = HERE / "direction_labels.json5"
# Each platform's area, from OpenStreetMap (`mta-od-data fetch-platforms`).
PLATFORM_AREAS = HERE / "platform_areas.csv"
DEFAULT_STATIONS = DATA / "stations.csv"
DEFAULT_COMPLEXES = DATA / "complexes.csv"
# A car is a length of train, so routes with different train lengths compare.
CAR_CHART_NOTE = f"*a car is {CAR_FT} ft of train"
CAR_NOTE = (
    f"\\* A car is {CAR_FT} ft of train, about one B Division car's length, "
    "so routes with different train lengths compare (`train_lengths.json5`)."
)


@dataclass(frozen=True, slots=True)
class Names:
    """Stations' and complexes' names, and stations' complexes and directions."""

    station: dict[str, str]
    complex_of: dict[str, str]
    complex: dict[str, str]
    direction: dict[tuple[str, str], str] = field(default_factory=dict)
    # Each station's name alone, without its routes.
    stop: dict[str, str] = field(default_factory=dict)


def load_names(stations: Path, complexes: Path) -> Names:
    """Names as the `analyze` reports write them: `abbreviate_name`d,
    with their routes as `display_station` lists them, `DeKalb Av (B,Q,R)`."""
    with stations.open() as f:
        rows = list(DictReader(f))
    complex_names = {
        str(c.complex_id): c.display()
        for c in Complex.load_all(complexes)
        if not isinstance(c, MissingComplex)
    }
    return Names(
        station={
            r["gtfs_stop_id"]: display_station(
                abbreviate_name(r["stop_name"]), frozenset(r["daytime_routes"].split())
            )
            for r in rows
        },
        complex_of={r["gtfs_stop_id"]: r["complex_id"] for r in rows},
        stop={r["gtfs_stop_id"]: abbreviate_name(r["stop_name"]) for r in rows},
        complex=complex_names,
        direction={
            (r["gtfs_stop_id"], d): r[f"{label}_direction_label"]
            for r in rows
            for d, label in [("N", "north"), ("S", "south")]
        },
    )


def busiest(
    rows: Iterable[tuple[Any, ...]],
) -> dict[tuple[Any, ...], tuple[int, float]]:
    """Each key's busiest hour and its riders, from `(*key, hour, riders)` rows:
    the earliest of any tied."""
    by_key: defaultdict[tuple[Any, ...], dict[int, float]] = defaultdict(dict)
    for *key, hour, riders in sorted(rows, key=as_text):
        hours = by_key[tuple(key)]
        hours[hour] = hours.get(hour, 0.0) + riders

    def most(hour_riders: tuple[int, float]) -> tuple[int, int]:
        hour, riders = hour_riders
        return (round(riders), -hour)

    return {k: max(hours.items(), key=most) for k, hours in by_key.items()}


def peak_heads(cols: Sequence[Column]) -> list[str]:
    return ["Peak Hour", f"Riders in Peak Hour, {cols[0].label}"]


def peak_cells(
    peaks: dict[tuple[Any, ...], tuple[int, float]], key: tuple[Any, ...]
) -> list[str]:
    if key not in peaks:
        return ["", ""]
    hour, riders = peaks[key]
    return [clock(hour), fmt(riders)]


def clock(hour: int) -> str:
    """A service day's hour, from 4 to 27, as the hour of the day it starts."""
    return clock_time(hour * 3600)


def as_text(row: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(map(str, row))


def by_riders(row: tuple[Any, ...]) -> tuple[int, str]:
    """A `(name, riders, ...)` row's order: busiest first, as shown."""
    return (-round(row[1]), row[0])


def by_line_then_riders(row: tuple[Any, ...]) -> tuple[str, int, str]:
    """A `(route, line, riders, ...)` row's order."""
    return (row[1], -round(row[2]), row[0])


def fmt(x: float | None, digits: int = 0) -> str:
    return f"{x or 0:,.{digits}f}"


# Station directions' labels, as short as `Uptown` or `Manhattan`.
COMPASS = {
    "Northbound": "NB",
    "Southbound": "SB",
    "Eastbound": "EB",
    "Westbound": "WB",
}


def platform_labels(names: Names, rows: list[tuple[Any, ...]]) -> dict[str, str]:
    """Each platform's station, from `platform_routes`' `rows`,
    and only as much more as tells it from the station's other platforms:
    the directions it serves,
    e.g. `96 St (1,2,3), Uptown`, or its routes, e.g. `Jamaica Center (E,J,Z), E`,
    then its routes each way, e.g. `Uptown 2,3`,
    then their express variants, e.g. `Uptown 7X`."""
    overrides = json5.loads(DIRECTION_LABELS.read_text(), allow_duplicate_keys=False)

    station: dict[str, str] = {}
    # Each way a platform serves, by its label: its routes that way.
    ways: defaultdict[str, defaultdict[str, list[str]]] = defaultdict(
        lambda: defaultdict(list)
    )
    # Each station's own labels, which a route's own label is shown without.
    own_labels: defaultdict[str, set[str]] = defaultdict(set)
    for platform, stop, d, rs in rows:
        station.setdefault(platform, names.station.get(stop, stop))
        override = overrides.get(stop, {})
        where = override.get(d, names.direction.get((stop, d), d))
        own_labels[platform].add(where)
        for r in rs:
            ways[platform][override[r][d] if r in override else where].append(r)
    # Each direction a platform serves: its label, its routes that way,
    # and whether the label is the routes' own, not the station's.
    served = {
        p: [
            (COMPASS.get(where, where), sorted(set(rs)), where not in own_labels[p])
            for where, rs in w.items()
        ]
        for p, w in ways.items()
    }

    def way(where: str, routes: Iterable[str]) -> str:
        return f"{where} {','.join(routes)}"

    def with_directions(p: str) -> str:
        # A train's last stop doesn't tell its platform: it's where it's going.
        wheres = dict.fromkeys(
            way(where, rs) if ours else where
            for where, rs, ours in served[p]
            if where != "Last Stop"
        )
        return f"{station[p]}, {' & '.join(wheres)}" if wheres else station[p]

    def routes_alone(p: str) -> str:
        routes = sorted({base_route(r) for _, rs, _ in served[p] for r in rs})
        return f"{station[p]}, {','.join(routes)}"

    def variants_alone(p: str) -> str:
        routes = sorted({r for _, rs, _ in served[p] for r in rs})
        return f"{station[p]}, {','.join(routes)}"

    def with_routes(p: str) -> str:
        ways = (
            way(where, sorted({base_route(r) for r in rs}))
            for where, rs, _ in served[p]
        )
        return f"{station[p]}, {' & '.join(ways)}"

    def with_variants(p: str) -> str:
        ways = (way(where, rs) for where, rs, _ in served[p])
        return f"{station[p]}, {' & '.join(ways)}"

    # Each station's platforms by the first of these that tells them all apart.
    platforms: defaultdict[str, list[str]] = defaultdict(list)
    for p, name in station.items():
        platforms[name].append(p)
    labels: dict[str, str] = {}
    for ps in platforms.values():
        for more in [
            station.__getitem__,
            with_directions,
            routes_alone,
            variants_alone,
            with_routes,
        ]:
            tried = {p: more(p) for p in ps}
            if len(set(tried.values())) == len(ps):
                break
        else:
            tried = {p: with_variants(p) for p in ps}
        labels |= tried
    return labels


def place_table(
    by: By,
    with_route: bool,
    rows: list[tuple[Any, ...]],
    hours: list[tuple[Any, ...]],
    platforms: list[tuple[Any, ...]],
    loads: list[tuple[Any, ...]],
    cols: list[Column],
    names_: Names,
) -> list[str]:
    """`place_rows`' rows as a table, with each place's busiest hour
    from `hours`, `(stop, dir, platform, [route,] hour, riders on + off)` rows,
    and for a platform, its area and its riders on and off per m² of it,
    and its most riders on it at once,
    from `loads`, `(stop, dir, platform, minute, riders)` rows."""
    platform_names = platform_labels(names_, platforms) if by is By.PLATFORM else {}
    areas: dict[str, float] = load_platform_areas() if by is By.PLATFORM else {}
    fixed = fix_platform_areas(areas, platforms)

    def label(stop: str, d: str, platform: str) -> tuple[str, ...]:
        match by:
            case By.COMPLEX:
                c = names_.complex_of.get(stop, "")
                return (names_.complex.get(c, c),)
            case By.STATION:
                return (names_.station.get(stop, stop),)
            case By.STATION_DIRECTION:
                where = names_.direction.get((stop, d), d)
                return names_.station.get(stop, stop), where
            case By.PLATFORM:
                if platform:
                    return (platform_names.get(platform, platform),)
                # A stop OSM's routes don't say the platform of: its direction.
                where = names_.direction.get((stop, d), d)
                name = names_.station.get(stop, stop)
                return (f"{name}, {where}, platform unknown",)
        raise AssertionError(by)

    # Complexes sum their stations' rows.
    k = len(cols)
    merged: defaultdict[tuple[str, ...], list[float]] = defaultdict(
        lambda: [0.0] * (k + 4)
    )

    def identity(stop: str, d: str, platform: str) -> tuple[str, ...]:
        """The place a row is at, which its name must be unique to."""
        match by:
            case By.COMPLEX:
                return (names_.complex_of.get(stop, ""),)
            case By.STATION:
                return (stop,)
            case By.STATION_DIRECTION:
                return (stop, d)
            case By.PLATFORM:
                return (platform,) if platform else (stop, d)
        raise AssertionError(by)

    named: dict[tuple[str, ...], tuple[str, ...]] = {}
    # In a set order, so a complex's floating-point sum of its stations is too.
    for row in sorted(rows, key=as_text):
        stop, d, platform, *rest = row
        grp = (rest.pop(0),) if with_route else ()
        key = (*label(stop, d, platform), *grp)
        place = identity(stop, d, platform)
        if named.setdefault(key, place) != place:
            raise ValueError(f"{named[key]} and {place} are both named {key}")
        for j, v in enumerate(rest):
            merged[key][j] += v or 0.0
    peaks = busiest((*label(stop, d, p), *rest) for stop, d, p, *rest in hours)
    most = {label(stop, d, p): (m, r) for stop, d, p, m, r in loads}
    head = [
        *(
            ["Station", "Direction"]
            if by is By.STATION_DIRECTION
            else [by.value.title()]
        ),
        *(["Route"] if with_route else []),
    ]
    lines = [
        table_row(
            *head,
            *(f"On + Off, {c.label}" for c in cols),
            f"On, {cols[0].label}",
            f"Off, {cols[0].label}",
            f"Transfers On + Off, {cols[0].label}",
            f"Staying On, {cols[0].label}",
            "Peak Hour",
            f"On + Off in Peak Hour, {cols[0].label}",
            *(
                [
                    "Area (m²)",
                    f"On + Off per m², {cols[0].label}",
                    f"On + Off in Peak Hour per m², {cols[0].label}",
                ]
                if areas
                else []
            ),
            *(
                [
                    "Most On Platform At",
                    f"Most On Platform, {cols[0].label}",
                    f"Most On Platform per m², {cols[0].label}",
                ]
                if most
                else []
            ),
        ),
        table_rule(
            "l" * len(head)
            + "r" * (k + 4)
            + "lr"
            + "rrr" * bool(areas)
            + "lrr" * bool(most)
        ),
    ]

    # By the riders as shown, so rows that show the same come out in a set order.
    def by_riders_shown(
        item: tuple[tuple[str, ...], list[float]],
    ) -> tuple[int, tuple[str, ...]]:
        key, vs = item
        return (-round(vs[0]), key)

    for key, vs in sorted(merged.items(), key=by_riders_shown):
        hour, riders = peaks.get(key, (None, 0.0))
        peak = (clock(hour), fmt(riders)) if hour is not None else ("", "")
        crowding: list[str] = []
        if areas:
            area = areas.get(named[key][0])
            mark = "†" if named[key][0] in fixed else ""
            crowding = (
                [fmt(area) + mark, fmt(vs[0] / area, 1), fmt(riders / area, 2)]
                if area
                else ["", "", ""]
            )
        on_platform: list[str] = []
        if most:
            at, n = most.get(key, (None, 0.0))
            area = areas.get(named[key][0])
            on_platform = (
                [clock_time(at * 60), fmt(n), fmt(n / area, 2) if area else ""]
                if at is not None
                else ["", "", ""]
            )
        lines.append(
            table_row(*key, *(fmt(v) for v in vs), *peak, *crowding, *on_platform)
        )
    if fixed:
        outlines = ", ".join(
            f"`{p}`, {fmt(own)} m², has `{big}`'s"
            for p, (own, big) in sorted(fixed.items())
        )
        lines += [
            "",
            f"† Its OpenStreetMap outline is under {PART_MAPPED:.0%} "
            "of another platform's at its station, so likely mapped only in part, "
            f"and it has that platform's area instead: {outlines}.",
        ]
    return lines


# A platform under this share of its station's biggest is taken to be mapped in part.
PART_MAPPED = 0.25


def fix_platform_areas(
    areas: dict[str, float], platforms: list[tuple[Any, ...]]
) -> dict[str, tuple[float, str]]:
    """Gives each platform of `areas` under `PART_MAPPED` of its stop's biggest
    the biggest's area, as its OpenStreetMap outline is likely only part of it,
    like Newkirk Plaza's southbound, 20 m of a 150 m platform.
    `platforms` are `platform_routes`' `(platform, stop, dir, routes)` rows.
    Each fixed platform's own area and the platform it now has the area of."""
    at: defaultdict[str, set[str]] = defaultdict(set)
    for platform, stop, *_ in platforms:
        if platform in areas:
            at[stop].add(platform)
    fixed: dict[str, tuple[float, str]] = {}
    for ps in at.values():
        big = max(sorted(ps), key=areas.__getitem__)
        for p in sorted(ps):
            if areas[p] < PART_MAPPED * areas[big] and p not in fixed:
                fixed[p] = (areas[p], big)
    for p, (_, big) in fixed.items():
        areas[p] = areas[big]
    return fixed


def load_platform_areas() -> dict[str, float]:
    """Each platform's area in m², by its OSM element, e.g. `w426103243`."""
    with PLATFORM_AREAS.open() as f:
        return {r["platform"]: float(r["area_m2"]) for r in DictReader(f)}


def route_order(riders: dict[str, float]) -> list[str]:
    """Busiest first, each route's variants right after it."""

    def order(g: str) -> tuple[int, str, bool, str]:
        base = base_route(g)
        return (-round(riders.get(base, 0.0)), base, g != base, g)

    return sorted(riders, key=order)


@app.command()
def ridership(
    ctx: Context,
    by: Annotated[
        list[By],
        Option(
            help=(
                "What to total riders by; repeat to cross one of "
                "complex, station, station-direction, or line with route"
            )
        ),
    ],
    route: Annotated[
        list[str] | None,
        Option(
            help=(
                "Only rides on these `--by route` rows (repeatable), "
                "e.g. --route 1, or --route N --route R --route W as one group"
            )
        ),
    ] = None,
    manifest: Annotated[
        Path, Option(help="`mta-od-data raptor assign-range`'s manifest")
    ] = DEFAULT_MANIFEST,
    od_factors: Annotated[
        list[Path] | None,
        Option(
            help=(
                "Count riders as if routed with OD data scaled by these factors "
                "(repeatable, a column each), from `mta-od-data scale-od`; "
                "by default 2019's counted entries"
            )
        ),
    ] = None,
    unscaled: Annotated[
        bool, Option(help="Count riders as in the OD data, unscaled, first")
    ] = True,
    fare_evasion: Annotated[
        bool,
        Option(
            help=(
                "Count fare evaders too: riders over 1 less the evasion rate "
                "in each date's quarter, or in the year scaled to"
            )
        ),
    ] = True,
    lines: Annotated[Path, Option(help="Named lines for --by line")] = DEFAULT_LINES,
    top: Annotated[
        int, Option(help="--by trip: each route's this many most crowded trains")
    ] = 1,
    markdown_out: Annotated[
        Path | None, Option(help="Write the report here, not to stdout")
    ] = None,
) -> None:
    """Average weekday ridership by station complex, station, station direction,
    route, or line,
    over `mta-od-data raptor assign-range`'s dates.
    """
    route = route or []
    if od_factors is None:
        od_factors = DEFAULT_OD_FACTORS
    dims = set(by)
    if By.TRIP in dims and len(dims) > 1:
        raise BadParameter("trip goes alone", param_hint="--by")
    places = dims & PLACES
    if By.TRIP not in dims and (
        len(dims) != len(by)
        or len(places) > 1
        or (places and By.LINE in dims)
        or (len(dims) > 1 and By.ROUTE not in dims)
    ):
        raise BadParameter(
            "one of complex, station, station-direction, route, or line, "
            "optionally crossed with route",
            param_hint="--by",
        )
    got = cached_compute(
        by, route, manifest, od_factors, unscaled, fare_evasion, lines, top
    )
    days, cols = got.days, got.cols
    if By.TRIP in dims:
        table = trip_table(
            got.trains,
            load_names(DEFAULT_STATIONS, DEFAULT_COMPLEXES),
            period(manifest),
        ) + ["", CAR_NOTE]
        label = period(manifest)
        charts = save_charts(
            markdown_out,
            table,
            2,
            chart_subtitle(manifest, fare_evasion),
            [
                Chart(
                    "peak-load",
                    "Each route's most crowded train",
                    [f"Peak Load, {label}"],
                    ["Peak load"],
                    label=peak_label,
                    align="rmlr",
                ),
                Chart(
                    "peak-per-car",
                    "Each route's most crowded train, per car*",
                    ["Peak per Car\\*"],
                    ["Peak per car"],
                    CAR_CHART_NOTE,
                    peak_label,
                    "rmlr",
                ),
            ],
        )
        report = render(ctx, by, route, manifest, days, [], fare_evasion, table, charts)
        write(report, markdown_out)
        return
    with_route = By.ROUTE in dims and len(dims) > 1

    if places:
        (place,) = places
        table = place_table(
            place,
            with_route,
            got.rows,
            got.hours,
            got.platforms,
            got.loads,
            cols,
            load_names(DEFAULT_STATIONS, DEFAULT_COMPLEXES),
        )
        keys = (2 if place is By.STATION_DIRECTION else 1) + with_route
        what = place.value.replace("-", " ")
        first = cols[0].label
        specs = [
            Chart(
                "riders",
                f"Riders on and off by {what}",
                [f"On + Off, {c.label}" for c in cols],
                [c.label for c in cols],
            )
        ]
        if place is By.PLATFORM and not with_route:
            specs += [
                Chart(
                    "per-m2",
                    "Riders on and off per m² of platform",
                    [f"On + Off per m², {first}"],
                    [first],
                ),
                Chart(
                    "peak-per-m2",
                    "Riders on and off in the peak hour per m² of platform",
                    [f"On + Off in Peak Hour per m², {first}"],
                    [first],
                    label=peak_hour_label,
                    align="rr",
                ),
                Chart(
                    "most-on-platform",
                    "Most riders on the platform at once",
                    [f"Most On Platform, {first}"],
                    [first],
                    label=most_on_label,
                    align="rr",
                ),
                Chart(
                    "most-on-platform-per-m2",
                    "Most riders on the platform at once per m²",
                    [f"Most On Platform per m², {first}"],
                    [first],
                    label=most_on_label,
                    align="rr",
                ),
            ]
    elif By.LINE in dims:
        if with_route:
            peaks = busiest(got.hours)
            table = [
                table_row("Line", "Route", *(c.label for c in cols), *peak_heads(cols)),
                table_rule("ll" + "r" * len(cols) + "lr"),
            ]
            for g, name, *vs in sorted(got.rows, key=by_line_then_riders):
                if not route or g in route:
                    table.append(
                        table_row(
                            name,
                            g,
                            *(fmt(v) for v in vs),
                            *peak_cells(peaks, (name, g)),
                        )
                    )
            keys = 2
            specs = [riders_chart("Riders by line and route", cols)]
        else:
            peaks = busiest(got.hours)
            table = [
                table_row("Line", *(c.label for c in cols), *peak_heads(cols)),
                table_rule("l" + "r" * len(cols) + "lr"),
            ]
            for name, *vs in sorted(got.rows, key=by_riders):
                table.append(
                    table_row(name, *(fmt(v) for v in vs), *peak_cells(peaks, (name,)))
                )
            keys = 1
            specs = [riders_chart("Riders by line", cols)]
    else:
        riders = {grp: vs for grp, *vs in got.rows}
        if route:
            riders = {g: vs for g, vs in riders.items() if g in route}
        peaks = busiest(got.hours)
        first = cols[0].label
        table = [
            table_row(
                "Route",
                *(c.label for c in cols),
                "Route-km",
                f"Per Route-km, {first}",
                "Trips",
                "Train-km",
                f"Per Train-km, {first}",
                f"Per Car\\*-km, {first}",
                *peak_heads(cols),
            ),
            table_rule("l" + "r" * (len(cols) + 6) + "lr"),
        ]
        for grp in route_order({g: vs[0] for g, vs in riders.items()}):
            s = got.service.get(grp, RouteService())
            vs = riders[grp]
            table.append(
                table_row(
                    grp,
                    *(fmt(v) for v in vs),
                    fmt(s.route_km, 1),
                    fmt(vs[0] / s.route_km if s.route_km else None),
                    fmt(s.trips),
                    fmt(s.train_km),
                    fmt(vs[0] / s.train_km if s.train_km else None, 1),
                    fmt(vs[0] / s.car_km if s.car_km else None, 2),
                    *peak_cells(peaks, (grp,)),
                )
            )

        table += ["", CAR_NOTE]
        keys = 1
        specs = [
            riders_chart("Riders by route", cols),
            Chart(
                "per-route-km",
                "Riders per route-km",
                [f"Per Route-km, {first}"],
                [first],
            ),
            Chart(
                "per-train-km",
                "Riders per train-km",
                [f"Per Train-km, {first}"],
                [first],
            ),
            Chart(
                "per-car-km",
                "Riders per car*-km",
                [f"Per Car\\*-km, {first}"],
                [first],
                CAR_CHART_NOTE,
            ),
        ]

    charts = save_charts(
        markdown_out, table, keys, chart_subtitle(manifest, fare_evasion), specs
    )
    report = render(ctx, by, route, manifest, days, cols, fare_evasion, table, charts)
    write(report, markdown_out)


def peak_label(row: Mapping[str, str]) -> list[str]:
    """Where and when a `trip_table` row's train is fullest,
    its route between the two stations: `Court Sq-23 St`, `F`, ...."""
    a, b = row["Peak Between"].split(" to ")
    return [a, row["Route"], b, row["Leaving At"]]


def peak_hour_label(row: Mapping[str, str]) -> list[str]:
    """A `place_table` row's place, and its peak hour."""
    return [row["Platform"], row["Peak Hour"]]


def most_on_label(row: Mapping[str, str]) -> list[str]:
    """A `place_table` row's platform, and when it's fullest."""
    return [row["Platform"], row["Most On Platform At"]]


def riders_chart(title: str, cols: Sequence[Column]) -> Chart:
    return Chart("riders", title, [c.label for c in cols], [c.label for c in cols])


def chart_subtitle(manifest: Path, fare_evasion: bool) -> str:
    dates = sorted(row["date"] for row in read_manifest(manifest))
    evaders = " with fare evaders" if fare_evasion else ""
    return f"Average weekday{evaders}, {dates[0]} to {dates[-1]}"


def save_charts(
    markdown_out: Path | None,
    table: list[str],
    keys: int,
    subtitle: str,
    specs: Sequence[Chart],
) -> list[tuple[str, str]]:
    """`specs`' charts of `table`, beside `markdown_out` as `<its name>-<slug>.svg`:
    each one's title and file name, for the report to show them."""
    if markdown_out is None:
        return []
    shown = []
    for spec, svg in zip(
        specs, table_charts(table, keys, subtitle, specs).values(), strict=True
    ):
        file = markdown_out.with_name(f"{markdown_out.stem}-{spec.slug}.svg")
        file.write_text(svg)
        shown.append((spec.title, file.name))
    return shown


def write(report: str, markdown_out: Path | None) -> None:
    if markdown_out is None:
        print(report, end="")
    else:
        markdown_out.write_text(report)
        print(f"Wrote {markdown_out}")


def clock_time(secs: int) -> str:
    """Seconds on the service day's clock as a time of day, `H:MM AM`."""
    hour = secs // 3600 % 24
    return f"{(hour - 1) % 12 + 1}:{secs % 3600 // 60:02} {'AM' if hour < 12 else 'PM'}"


def trip_table(trains: list[Train], names: Names, label: str) -> list[str]:
    def stop(s: str) -> str:
        return names.stop.get(s, s)

    lengths = load_train_lengths()

    lines = [
        table_row(
            "Route",
            "Train",
            f"Peak Load, {label}",
            "Train Length (ft)",
            "Peak per Car\\*",
            "Peak Between",
            "Leaving At",
            "Weekdays Run",
        ),
        table_rule("llrrrllr"),
    ]
    for t in trains:
        lines.append(
            table_row(
                t.route,
                f"{clock_time(t.first_departure)} {stop(t.first_stop)}"
                f" to {stop(t.last_stop)}",
                fmt(t.peak),
                fmt(lengths.get(t.route)),
                fmt(t.peak / lengths[t.route] * CAR_FT if t.route in lengths else None),
                f"{stop(t.peak_stop)} to {stop(t.peak_next)}",
                clock_time(t.peak_departure),
                str(t.days),
            )
        )
    return lines


def render(
    ctx: Context,
    by: Iterable[By],
    route: Sequence[str],
    manifest: Path,
    days: int,
    cols: Sequence[Column],
    fare_evasion: bool,
    table: list[str],
    charts: Sequence[tuple[str, str]] = (),
) -> str:
    dates = sorted(row["date"] for row in read_manifest(manifest))
    scope = f" on {', '.join(route)}" if route else ""
    evaders = " with fare evaders" if fare_evasion else ""
    lines = [
        f"# Ridership by {' and '.join(b.value.replace('-', ' ') for b in by)}{scope}",
        "",
        f"Average weekday riders{evaders}, "
        f"over {days} weekdays from {dates[0]} to {dates[-1]} "
        f"(`{manifest}`).",
        *(
            f"The {c.label} column scales the OD data on these dates "
            f"to {c.scaled_to}'s counted station entries."
            for c in cols
            if c.scaled_to is not None
        ),
        *(
            [
                "The peak hour is the hour, by when it starts, "
                f"with the most riders in the {cols[0].label} column "
                "on its trains there "
                "(getting on or off at a place, boarding a route, or joining a line), "
                "and those riders."
            ]
            if cols
            else [
                "A train's load is its riders on board between two stops, "
                "averaged over the weekdays it runs: "
                "a train is the same on any date with the same route, direction, "
                "first stop, and departure from it."
            ]
        ),
        *(
            [
                "Platforms are from OpenStreetMap's subway routes "
                "(© OpenStreetMap contributors, ODbL), "
                "by `mta-od-data fetch-platforms`.",
                "A platform's area is its OpenStreetMap outline's, "
                "and its On + Off per m² is its riders getting on or off "
                "over the day, or the peak hour, per m² of it: "
                "how busy it is for its size, not how many stand on it at once.",
            ]
            if By.PLATFORM in by
            else []
        ),
        "",
        f"Produced by `{produced_by(ctx)}`.",
        "",
        # Each under its own heading, to link to, and collapsible, as they're long:
        # GitHub keeps `<details>`, but not the styles a scrolling box would take.
        "## Table",
        "",
        "<details open>",
        "<summary>The table</summary>",
        "",
        *table,
        "",
        "</details>",
        *(["", "## Charts"] if charts else []),
        *(
            line
            for title, file in charts
            for line in (
                "",
                f"### {escaped(title)}",
                "",
                "<details>",
                "<summary>The chart</summary>",
                "",
                f"![{escaped(title)}]({file})",
                "",
                "</details>",
            )
        ),
    ]
    return "\n".join(lines) + "\n"


def escaped(title: str) -> str:
    """A chart's title as Markdown text: its `*`s, the car note's, kept literal."""
    return title.replace("*", r"\*")
