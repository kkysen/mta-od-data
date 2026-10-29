"""The MBTA's GTFS, which has `pathways.txt` as the MTA's doesn't yet,
for testing RAPTOR's pathways transfers:
a pinned version, and a small fixture cut from it for `cargo test`.

The data is MassDOT's, under its Developers License Agreement
(https://github.com/mbta/gtfs-documentation/blob/master/developers-license-agreement.pdf),
which lets us reproduce and redistribute it, acknowledging MassDOT as its provider.
"""

import csv
import hashlib
import io
from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Annotated
from urllib.request import urlretrieve
from zipfile import ZipFile

from typer import Option, Typer

from mta_od_data import DATA, ROOT

app = Typer()

# "Fall 2026, 2026-10-27T19:47:13+00:00, version D", from 2026-10-20 to 2026-12-12,
# from https://cdn.mbta.com/archive/archived_feeds.txt.
URL = "https://cdn.mbtace.com/archive/20261020.zip"
SHA256 = "fdbbe7903ee7519edf3728df9ba65da18e17cb193545169daaf0763d1e44131c"
DEFAULT_FEED = DATA / "mbta-gtfs" / "20261020.zip"
DEFAULT_FIXTURE = ROOT / "raptor" / "tests" / "data" / "mbta-downtown"

# Park St, Downtown Crossing, Government Center, and North Station:
# an island, Green Line berths, a concourse between two stations,
# and commuter rail behind gates of its own.
STATIONS = {"place-pktrm", "place-dwnxg", "place-gover", "place-north"}
DAY = date(2026, 10, 28)
# Trips stopping in the fixture between these, on the service day's clock.
FROM, UNTIL = "07:00:00", "10:00:00"
# Light rail and subway.
ROUTE_TYPES = {"0", "1"}

README = f"""\
A subset of the MBTA's GTFS, for `cargo test`, cut by `mta-od-data fetch-mbta`:
its stations {", ".join(sorted(STATIONS))}, and their light rail and subway trips
stopping there from {FROM} to {UNTIL} on {DAY}, only at those stations.

Data provided by MassDOT, under its Developers License Agreement:
https://github.com/mbta/gtfs-documentation/blob/master/developers-license-agreement.pdf
From {URL}
(sha256 {SHA256}).
"""


def rows(feed: ZipFile, name: str) -> Iterator[dict[str, str]]:
    with feed.open(name) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig"))


def write(out: Path, name: str, fields: list[str], kept: list[dict[str, str]]) -> None:
    with (out / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept)
    print(f"wrote {out / name}: {len(kept)} rows")


def header(feed: ZipFile, name: str) -> list[str]:
    with feed.open(name) as f:
        return next(csv.reader(io.TextIOWrapper(f, encoding="utf-8-sig")))


def services_on(feed: ZipFile, day: date) -> set[str]:
    weekday = f"{day:%A}".lower()
    ymd = f"{day:%Y%m%d}"
    services = {
        r["service_id"]
        for r in rows(feed, "calendar.txt")
        if r[weekday] == "1" and r["start_date"] <= ymd <= r["end_date"]
    }
    for r in rows(feed, "calendar_dates.txt"):
        if r["date"] == ymd:
            if r["exception_type"] == "1":
                services.add(r["service_id"])
            else:
                services.discard(r["service_id"])
    return services


@app.command()
def fetch_mbta(
    feed: Annotated[
        Path, Option(help="The pinned MBTA GTFS version, fetched if missing")
    ] = DEFAULT_FEED,
    fixture: Annotated[
        Path, Option(help="Where the subset for `cargo test` goes")
    ] = DEFAULT_FIXTURE,
) -> None:
    """Fetch the pinned MBTA GTFS version,
    and cut from it the fixture RAPTOR's pathways tests read."""
    if not feed.exists():
        feed.parent.mkdir(parents=True, exist_ok=True)
        print(f"fetching {URL}")
        urlretrieve(URL, feed)
    digest = hashlib.sha256(feed.read_bytes()).hexdigest()
    if digest != SHA256:
        raise SystemExit(f"{feed}: sha256 {digest}, not the pinned {SHA256}")
    fixture.mkdir(parents=True, exist_ok=True)

    with ZipFile(feed) as z:
        stops = [
            r
            for r in rows(z, "stops.txt")
            if r["stop_id"] in STATIONS or r["parent_station"] in STATIONS
        ]
        stop_ids = {r["stop_id"] for r in stops}
        routes = {
            r["route_id"]
            for r in rows(z, "routes.txt")
            if r["route_type"] in ROUTE_TYPES
        }
        services = services_on(z, DAY)
        trips = {
            r["trip_id"]: r
            for r in rows(z, "trips.txt")
            if r["route_id"] in routes and r["service_id"] in services
        }
        stop_times: dict[str, list[dict[str, str]]] = {}
        for r in rows(z, "stop_times.txt"):
            if r["trip_id"] in trips and r["stop_id"] in stop_ids:
                stop_times.setdefault(r["trip_id"], []).append(r)
        # Zero-padded `HH:MM:SS`, so compared as text.
        kept = {
            t: sts
            for t, sts in stop_times.items()
            if len(sts) >= 2
            and all(FROM <= st["departure_time"].zfill(8) <= UNTIL for st in sts)
        }
        used = {trips[t]["service_id"] for t in kept}

        write(fixture, "stops.txt", header(z, "stops.txt"), stops)
        write(
            fixture,
            "trips.txt",
            header(z, "trips.txt"),
            [trips[t] for t in sorted(kept)],
        )
        write(
            fixture,
            "stop_times.txt",
            header(z, "stop_times.txt"),
            [st for t in sorted(kept) for st in kept[t]],
        )
        for name in ["calendar.txt", "calendar_dates.txt"]:
            write(
                fixture,
                name,
                header(z, name),
                [r for r in rows(z, name) if r["service_id"] in used],
            )
        for name in ["pathways.txt", "transfers.txt"]:
            write(
                fixture,
                name,
                header(z, name),
                [
                    r
                    for r in rows(z, name)
                    if r["from_stop_id"] in stop_ids and r["to_stop_id"] in stop_ids
                ],
            )
    (fixture / "README.md").write_text(README)
