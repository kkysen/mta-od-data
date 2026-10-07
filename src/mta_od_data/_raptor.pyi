"""RAPTOR journey assignment, from the `raptor` crate (`raptor/src/lib.rs`)."""

from datetime import date
from os import PathLike
from pathlib import Path
from typing import final

type StrPath = str | PathLike[str]

MAX_RIDES: int

@final
class Version:
    """A feed version zip, with its `calendar.txt` span."""

    @staticmethod
    def open(path: StrPath) -> Version: ...
    @property
    def path(self) -> Path: ...
    @property
    def start(self) -> date: ...
    @property
    def end(self) -> date: ...

@final
class AssignSummary:
    riders_in: float
    riders_assigned: float
    unassigned_no_stops: float
    unassigned_unreachable: float
    unassigned_no_departure: float
    paths: int
    report: str

def load_versions(dir: StrPath) -> list[Version]: ...
def pick_weekdays(
    versions: list[Version], start: date, end: date
) -> list[tuple[date, Version, int]]: ...
def assign_date(
    version: Version,
    date: date,
    od: StrPath,
    stations: StrPath,
    config: StrPath,
    out: StrPath,
) -> AssignSummary: ...
def feed_report(feed: StrPath) -> str: ...
def timetable_report(feed: StrPath, date: date) -> str: ...
def route_report(
    feed: StrPath,
    date: date,
    origins: list[str],
    destinations: list[str],
    depart: str,
) -> str: ...
def profile_report(
    feed: StrPath,
    date: date,
    origins: list[str],
    destinations: list[str],
    after: str,
    before: str,
) -> str: ...
def od_report(feed: StrPath, date: date, od: StrPath, stations: StrPath) -> str: ...
