from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from mta_od_data.analyze import Station


@dataclass(slots=True)
class Region:
    name: str
    contains: Callable[[Station], bool]


def borough_region(name: str, boroughs: set[str]) -> Region:
    return Region(name=name, contains=lambda s: s.borough in boroughs)


def cbd_region() -> Region:
    """Manhattan's Congestion Relief Zone (the congestion-pricing/Hub Bound
    Report sense of "Lower Manhattan": below 60th St). Backed by the source
    data's own curated `cbd` flag rather than a latitude cut -- Manhattan's
    grid is rotated relative to true north, so no single latitude cleanly
    separates the zone, and a latitude cut would also wrongly include
    Roosevelt Island (south of 60th St by latitude, but not part of the
    zone), which `cbd` correctly excludes."""
    return Region(
        name="Lower Manhattan (below 60th St / Congestion Relief Zone)",
        contains=lambda s: s.cbd,
    )


@dataclass(slots=True)
class BoundingBox:
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

    def contains_coord(self, lat: float, lon: float) -> bool:
        return (
            self.min_lat <= lat <= self.max_lat and self.min_lon <= lon <= self.max_lon
        )


def bbox_region(name: str, bbox: BoundingBox) -> Region:
    return Region(
        name=name, contains=lambda s: bbox.contains_coord(s.loc.lat, s.loc.lon)
    )


def parse_bbox(s: str) -> BoundingBox:
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 4:
        raise ValueError(
            f"expected MIN_LAT,MIN_LON,MAX_LAT,MAX_LON (4 comma-separated "
            f"numbers), got {s!r}"
        )
    min_lat, min_lon, max_lat, max_lon = (float(p) for p in parts)
    return BoundingBox(
        min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon
    )


class RegionPreset(StrEnum):
    CBD = "cbd"
    MANHATTAN = "manhattan"
    BROOKLYN = "brooklyn"
    QUEENS = "queens"
    BRONX = "bronx"
    STATEN_ISLAND = "staten-island"


# Borough codes as given by the source data (stations_complexes.csv/
# stations_individual.csv's `borough` column).
PRESET_BOROUGH_CODES: dict[RegionPreset, set[str]] = {
    RegionPreset.MANHATTAN: {"M"},
    RegionPreset.BROOKLYN: {"Bk"},
    RegionPreset.QUEENS: {"Q"},
    RegionPreset.BRONX: {"Bx"},
    RegionPreset.STATEN_ISLAND: {"SI"},
}

PRESET_LABELS: dict[RegionPreset, str] = {
    RegionPreset.MANHATTAN: "Manhattan",
    RegionPreset.BROOKLYN: "Brooklyn",
    RegionPreset.QUEENS: "Queens",
    RegionPreset.BRONX: "Bronx",
    RegionPreset.STATEN_ISLAND: "Staten Island",
}


def region_from_preset(preset: RegionPreset) -> Region:
    if preset == RegionPreset.CBD:
        return cbd_region()
    return borough_region(PRESET_LABELS[preset], PRESET_BOROUGH_CODES[preset])
