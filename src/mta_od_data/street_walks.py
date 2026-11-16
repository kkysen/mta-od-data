"""The streets `mta-od-data raptor assign --street-walks` walks between stations on,
out one entrance and in another, to change trains between complexes on
(`raptor/src/walks.rs`), each run, with its own config's speeds.

The streets are cut from Geofabrik's New York extract
to what's walked on near the stations,
about 20 MB of its 500,
as `streets` keeps every node of what it reads in memory.
"""

from csv import DictReader
from pathlib import Path
from urllib.request import urlretrieve

import osmium
import osmium.osm

from mta_od_data import DATA
from mta_od_data.platforms import DEFAULT_EXTRACT, EXTRACT_URL
from mta_od_data.prepare import DEFAULT_STATIONS_CSV

DEFAULT_STREETS = DATA / "osm" / "nyc-streets.osm.pbf"

# How far past the stations to keep streets, in degrees (about 2 km),
# more than any walk between them (`TRANSFER_LIMIT`, 15 minutes) reaches.
MARGIN = 0.02

# What `streets` builds its walking network from, as R5 did,
# besides streets, sidewalks, footpaths, and steps, which are all `highway`.
PLATFORM_TAGS = {("railway", "platform"), ("public_transport", "platform")}


def _walkable(way: osmium.osm.Way) -> bool:
    return "highway" in way.tags or any(
        way.tags.get(key) == value for key, value in PLATFORM_TAGS
    )


def station_bounds(stations: Path) -> tuple[float, float, float, float]:
    """`(min_lat, min_lon, max_lat, max_lon)` around `stations`' coordinates,
    `MARGIN` out."""
    with stations.open(newline="") as f:
        points = [
            (float(r["gtfs_latitude"]), float(r["gtfs_longitude"]))
            for r in DictReader(f)
        ]
    lats, lons = zip(*points, strict=True)
    return (
        min(lats) - MARGIN,
        min(lons) - MARGIN,
        max(lats) + MARGIN,
        max(lons) + MARGIN,
    )


def filter_streets(
    extract: Path, dest: Path, bounds: tuple[float, float, float, float]
) -> int:
    """Write the ways in `extract` that routing walks on within `bounds` to `dest`,
    with the nodes they use. Returns how many ways were kept."""
    min_lat, min_lon, max_lat, max_lon = bounds

    def in_bounds(way: osmium.osm.Way) -> bool:
        return any(
            node.location.valid()
            and min_lon <= node.location.lon <= max_lon
            and min_lat <= node.location.lat <= max_lat
            for node in way.nodes
        )

    # `osmium` tells the format from the extension, so `.partial` goes before it.
    partial = dest.with_name(dest.name.replace(".osm.pbf", ".partial.osm.pbf"))
    kept = 0
    # Node tags are kept, for barriers, crossings, and the like.
    with osmium.BackReferenceWriter(
        partial, ref_src=extract, overwrite=True, remove_tags=False
    ) as w:
        # Nodes are read only for the locations of ways' nodes;
        # `w` adds the ones it needs.
        processor = osmium.FileProcessor(extract, osmium.osm.NODE | osmium.osm.WAY)
        for obj in processor.with_locations():
            if isinstance(obj, osmium.osm.Way) and _walkable(obj) and in_bounds(obj):
                w.add_way(obj)
                kept += 1
    partial.rename(dest)
    return kept


def fetch_extract(extract: Path = DEFAULT_EXTRACT) -> Path:
    """Geofabrik's New York extract, fetched if missing."""
    if not extract.exists():
        extract.parent.mkdir(parents=True, exist_ok=True)
        print(f"fetching {EXTRACT_URL}")
        # Beside it and renamed into place, so an interrupted fetch leaves no extract.
        part = extract.with_name(f"{extract.name}.part")
        urlretrieve(EXTRACT_URL, part)
        part.replace(extract)
    return extract


def cut(
    extract: Path = DEFAULT_EXTRACT,
    streets: Path = DEFAULT_STREETS,
    stations: Path = DEFAULT_STATIONS_CSV,
) -> Path:
    """`streets`, cut from `extract`, fetched if missing,
    unless `streets` is newer than it."""
    fetch_extract(extract)
    if not streets.exists() or streets.stat().st_mtime < extract.stat().st_mtime:
        kept = filter_streets(extract, streets, station_bounds(stations))
        print(f"cut {kept} ways to {streets}")
    return streets
