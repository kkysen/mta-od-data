"""`od_parquet` leaves a Parquet that's there alone, and downloads one that isn't."""

from pathlib import Path

import pytest

from mta_od_data import downloads
from mta_od_data.downloads import od_parquet


def test_kept_when_there(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "mta_od_2026.parquet"
    path.write_bytes(b"rows")

    def no_download(*args: object, **kwargs: object) -> None:
        raise AssertionError("downloaded again")

    monkeypatch.setattr(downloads.subprocess, "run", no_download)
    assert od_parquet(path) == path


def test_downloaded_whole(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "mta_od_2026.parquet"
    calls: list[list[str]] = []

    def download(args: list[str], check: bool) -> None:
        calls.append(args)
        Path(args[args.index("--output") + 1]).write_bytes(b"rows")

    monkeypatch.setattr(downloads.subprocess, "run", download)
    assert od_parquet(path) == path
    assert path.read_bytes() == b"rows"
    assert not path.with_name(f"{path.name}.part").exists()
    assert calls[0][:4] == ["gh", "release", "download", "od-data"]
    assert calls[0][calls[0].index("--pattern") + 1] == "mta_od_2026.parquet"
