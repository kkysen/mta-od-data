"""Which transfers out of the system would save riders the most time if they were free.

Compares two runs of `mta-od-data raptor assign-range` over the same dates:
one as today, where the only transfers out of the system
are the free ones `transfers.txt` has
(Lexington Av/59 St and 63 St, Junius St and Livonia Av),
and one with `--street-walks`, changing trains between any complexes on the streets,
out one entrance and in another, with no fare.

Each OD row's time saved is its mean journey as today
less each of its paths' with free transfers, by its riders on each path:
from entering at its origin to leaving the train at its destination.
A path's saving is split evenly between the transfers out of the system it makes,
grouped by the two complexes each joins, either way.
Paths making none can save or lose a little too,
as riders split between journeys by their cost (`raptor/assign.json5`),
and some can take a slower one when quicker ones are added;
those are counted, not attributed.

Every transfer is free at once, so two that serve the same riders split them,
and either alone would save more than its share here.
"""

import sys
from csv import DictReader, DictWriter
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

from duckdb import DuckDBPyConnection
from typer import Context, Option, Typer

from mta_od_data import DATA
from mta_od_data.analyze.common import connection
from mta_od_data.analyze.markdown import table_row, table_rule
from mta_od_data.analyze.path_riders import DatePaths, date_paths, read_manifest
from mta_od_data.invocation import produced_by
from mta_od_data.prepare import DEFAULT_COMPLEXES_CSV, DEFAULT_STATIONS_CSV

app = Typer()

DEFAULT_TODAY = DATA / "raptor" / "manifest.csv"
DEFAULT_FREE = DATA / "raptor-street" / "manifest.csv"


def street_transfers(d: DatePaths) -> Path:
    """The transfers `--street-walks` added on `d`'s date, beside its paths."""
    return d.paths.with_name(f"street-transfers-{d.day}.csv")


# Each OD row's riders and mean journey as today, in seconds.
_TODAY = """
    CREATE OR REPLACE TEMP TABLE today AS
    SELECT hour, origin, destination,
        sum(riders)::DOUBLE AS riders,
        sum(riders * (wait_s + in_vehicle_s + walk_s))::DOUBLE / sum(riders) AS secs
    FROM read_parquet($paths)
    WHERE origin <> destination
    GROUP BY ALL
"""

# Each path with free transfers' transfers out of the system, by station,
# and how many it makes.
_TRANSFERS = """
    CREATE OR REPLACE TEMP TABLE transfers AS
    WITH legs AS (
        SELECT path_id, unnest(string_split(path, ' | ')) AS leg
        FROM read_parquet($texts)
    ),
    walks AS (
        SELECT path_id,
            regexp_extract(leg, '^walk ([^>]+)>(.+)$', 1) AS a,
            regexp_extract(leg, '^walk ([^>]+)>(.+)$', 2) AS b
        FROM legs
        WHERE leg LIKE 'walk %'
    )
    SELECT path_id, a, b, count(*) OVER (PARTITION BY path_id) AS n
    FROM walks
    SEMI JOIN read_csv($added, all_varchar = true) x
        ON x.from_stop_id = walks.a AND x.to_stop_id = walks.b
"""

# Each path with free transfers' riders and their seconds saved, by OD row.
_FREE = """
    CREATE OR REPLACE TEMP TABLE free AS
    SELECT f.path_id, f.riders::DOUBLE AS riders,
        f.riders::DOUBLE * (t.secs - (f.wait_s + f.in_vehicle_s + f.walk_s)) AS saved
    FROM read_parquet($paths) f
    JOIN today t USING (hour, origin, destination)
"""


@dataclass(slots=True)
class Pair:
    """Transfers between two complexes, either way, averaged over a day."""

    complexes: tuple[str, str]
    # Riders making it each way, by `complexes`' order.
    riders: list[float]
    # Rider-seconds saved, split among each path's transfers.
    saved: float = 0.0
    # The shortest walk between them, in seconds.
    walk: int | None = None

    @property
    def total_riders(self) -> float:
        return sum(self.riders)


@dataclass(slots=True)
class Totals:
    riders: float = 0.0
    with_transfers: float = 0.0
    saved_with: float = 0.0
    saved_without: float = 0.0


def _complex_of(stations: Path) -> dict[str, str]:
    with stations.open(newline="") as f:
        return {r["gtfs_stop_id"]: r["complex_id"] for r in DictReader(f)}


def _names(complexes: Path) -> dict[str, str]:
    with complexes.open(newline="") as f:
        return {r["complex_id"]: r["display_name"] for r in DictReader(f)}


def _one(db: DuckDBPyConnection, query: str) -> tuple[float, float]:
    """`query`'s one row, of two numbers."""
    row = db.execute(query).fetchone()
    assert row is not None
    return float(row[0]), float(row[1])


def compare(
    today: Path, free: Path, stations: Path
) -> tuple[dict[tuple[str, str], Pair], Totals, int]:
    """Each pair of complexes' transfers out of the system,
    and the totals, averaged over the dates both manifests route, by their days,
    and how many days that is."""
    complex_of = _complex_of(stations)
    today_rows = {row["date"]: row for row in read_manifest(today)}
    free_rows = [row for row in read_manifest(free) if row["date"] in today_rows]
    if not free_rows:
        raise SystemExit(f"error: {today} and {free} route no date in common")
    days = sum(int(row["days"]) for row in free_rows)
    pairs: dict[tuple[str, str], Pair] = {}
    totals = Totals()
    db = connection()
    for row in free_rows:
        weight = int(row["days"]) / days
        base = date_paths(today, today_rows[row["date"]])
        d = date_paths(free, row)
        added = street_transfers(d)
        db.execute(_TODAY, {"paths": str(base.paths)})
        db.execute(_TRANSFERS, {"texts": str(d.texts), "added": str(added)})
        db.execute(_FREE, {"paths": str(d.paths)})
        riders, saved = _one(db, "SELECT sum(riders), sum(saved) FROM free")
        with_riders, with_saved = _one(
            db,
            "SELECT coalesce(sum(riders), 0), coalesce(sum(saved), 0) FROM free "
            "SEMI JOIN transfers USING (path_id)",
        )
        totals.riders += weight * riders
        totals.with_transfers += weight * with_riders
        totals.saved_with += weight * with_saved
        totals.saved_without += weight * (saved - with_saved)
        by_stations = db.execute(
            """
            SELECT t.a, t.b, sum(f.riders), sum(f.saved / t.n)
            FROM free f JOIN transfers t USING (path_id)
            GROUP BY ALL
            """
        ).fetchall()
        for a, b, riders, saved in by_stations:
            ca, cb = complex_of[a], complex_of[b]
            key = (ca, cb) if ca < cb else (cb, ca)
            pair = pairs.setdefault(key, Pair(key, [0.0, 0.0]))
            pair.riders[0 if key[0] == ca else 1] += weight * riders
            pair.saved += weight * saved
        with added.open(newline="") as f:
            for r in DictReader(f):
                ca = complex_of[r["from_stop_id"]]
                cb = complex_of[r["to_stop_id"]]
                key = (ca, cb) if ca < cb else (cb, ca)
                if (pair := pairs.get(key)) is not None:
                    walk = int(r["walk"])
                    pair.walk = walk if pair.walk is None else min(pair.walk, walk)
    return pairs, totals, days


def _duration(secs: float) -> str:
    """`secs` as `m:ss`, or `h:mm:ss` from an hour."""
    m, s = divmod(round(secs), 60)
    h, m = divmod(m, 60)
    return f"{h:,}:{m:02}:{s:02}" if h else f"{m}:{s:02}"


def _hours(secs: float) -> str:
    """A day's rider time, `secs`, as `h:mm`."""
    h, m = divmod(round(secs / 60), 60)
    return f"{h:,}:{m:02}"


def render_markdown(
    pairs: list[Pair], totals: Totals, names: dict[str, str], top_n: int
) -> str:
    saved = totals.saved_with + totals.saved_without
    lines = [
        "## Summary",
        "",
        table_row("Measure", "Value"),
        table_rule("lr"),
        table_row("Riders on an average weekday", f"{totals.riders:,.0f}"),
        table_row(
            "Riders making a free transfer out of the system",
            f"({totals.with_transfers / totals.riders:.1%}) "
            f"{totals.with_transfers:,.0f}",
        ),
        table_row("Rider time saved a day (h:mm)", _hours(saved)),
        table_row("By riders making a free transfer", _hours(totals.saved_with)),
        table_row(
            "By the rest, splitting differently (not attributed)",
            _hours(totals.saved_without),
        ),
        table_row(
            "Time saved per rider making one",
            _duration(totals.saved_with / totals.with_transfers),
        ),
        "",
        f"## The {min(top_n, len(pairs))} transfers saving the most",
        "",
        "Each way's riders are in the order the transfer names its complexes.",
        "",
        "| # | Transfer | Walk | Riders a day | Each way "
        "| Rider time saved a day (h:mm) | Time saved per rider |",
        table_rule("rlrrrrr"),
    ]
    for i, p in enumerate(pairs[:top_n], 1):
        a, b = (names.get(c, c) for c in p.complexes)
        lines.append(
            table_row(
                str(i),
                f"{a} ↔ {b}",
                "" if p.walk is None else _duration(p.walk),
                f"{p.total_riders:,.0f}",
                f"{p.riders[0]:,.0f} / {p.riders[1]:,.0f}",
                _hours(p.saved),
                _duration(p.saved / p.total_riders),
            )
        )
    return "\n".join(lines) + "\n"


CSV_FIELDS = [
    "complex_a",
    "complex_b",
    "name_a",
    "name_b",
    "walk_s",
    "riders",
    "riders_a_to_b",
    "riders_b_to_a",
    "rider_hours_saved",
]


@app.command()
def free_transfers(
    ctx: Context,
    today: Annotated[
        Path,
        Option(help="`assign-range`'s manifest as today, without `--street-walks`"),
    ] = DEFAULT_TODAY,
    free: Annotated[
        Path,
        Option(help="`assign-range --street-walks`' manifest, over the same dates"),
    ] = DEFAULT_FREE,
    stations: Annotated[
        Path, Option(help="The station reference CSV")
    ] = DEFAULT_STATIONS_CSV,
    complexes: Annotated[
        Path, Option(help="The complex reference CSV, for names")
    ] = DEFAULT_COMPLEXES_CSV,
    top_n: Annotated[int, Option(help="Transfers to list in the report")] = 50,
    csv_out: Annotated[Path | None, Option(help="Every transfer, as CSV")] = None,
    markdown_out: Annotated[Path | None, Option(help="The report")] = None,
) -> None:
    """Which transfers out of the system would save riders the most time if free,
    and how much."""
    pairs_by_key, totals, days = compare(today, free, stations)
    pairs = sorted(pairs_by_key.values(), key=lambda p: (-p.saved, p.complexes))
    names = _names(complexes)
    report = render_markdown(pairs, totals, names, top_n)
    print(report)
    if csv_out:
        with csv_out.open("w", newline="") as f:
            out = DictWriter(f, CSV_FIELDS, lineterminator="\n")
            out.writeheader()
            for p in pairs:
                a, b = p.complexes
                out.writerow(
                    {
                        "complex_a": a,
                        "complex_b": b,
                        "name_a": names.get(a, a),
                        "name_b": names.get(b, b),
                        "walk_s": p.walk,
                        "riders": round(p.total_riders, 2),
                        "riders_a_to_b": round(p.riders[0], 2),
                        "riders_b_to_a": round(p.riders[1], 2),
                        "rider_hours_saved": round(p.saved / 3600, 2),
                    }
                )
        print(f"wrote {csv_out}", file=sys.stderr)
    if markdown_out:
        preamble = [
            "# Free transfers out of the system",
            "",
            "Which transfers out of the system would save riders the most time "
            "if they were free, on an average weekday "
            f"({days} weekdays, as `assign-range` routes them): "
            "routed as today, where the only free ones are "
            "Lexington Av/59 St and 63 St's and Junius St and Livonia Av's, "
            "and with every walk between complexes on the streets free, "
            "out one entrance and in another, all at once.",
            "",
            "A path's time saved is its OD row's mean journey as today less its own, "
            "from entering to leaving the train, "
            "split evenly between the transfers out of the system it makes. "
            "Two transfers serving the same riders split them, "
            "so either alone would save more than its share here. "
            "Changes between a complex's stations take `transfers.txt`'s flat times, "
            "mostly 180s, until the MTA publishes pathways. "
            "See `free_transfers.py` for the rest.",
            "",
            f"Produced by `{produced_by(ctx)}`.",
            "",
        ]
        markdown_out.write_text("\n".join([*preamble, ""]) + report)
        print(f"wrote {markdown_out}", file=sys.stderr)
