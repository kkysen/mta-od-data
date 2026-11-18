#!/usr/bin/env bash
# Profile the `raptor` extension's heap with `dhat` while it assigns one date.
#
# Usage: scripts/profile-heap.sh [--date <date>]
#
# Builds the extension with the `dhat-heap` feature (`dhat`'s allocator, not `mimalloc`),
# assigns the date, and writes `dhat-heap.json` to `.scratch/dhat/`,
# viewable in DHAT's viewer (https://nnethercote.github.io/dh_view/dh_view.html).
# Then rebuilds the extension as usual.
#
# `dhat` records every allocation's backtrace, so a full date takes many minutes.

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

date=2025-10-15
while (($#)); do
    case "$1" in
        --date) date="$2"; shift 2 ;;
        *) echo "unknown argument $1" >&2; exit 1 ;;
    esac
done

# On disk, not in `/tmp` (tmpfs, RAM), in the repo's scratch folder.
out="$root/.scratch/dhat"
mkdir -p "$out"

cd "$root"
echo "building with dhat"
MATURIN_PEP517_ARGS="--features dhat-heap" CARGO_PROFILE_RELEASE_DEBUG=line-tables-only \
    uv sync --quiet --reinstall-package mta-od-data

echo "assigning $date"
# `dhat` writes to the working directory.
(
    cd "$out"
    # Through the Rust function itself, so `dhat` profiles nothing but the assignment.
    "$root/.venv/bin/python" - "$date" "$out/paths.parquet" 2>&1 <<'EOF' \
        | rg '^dhat:' || true
import sys
from datetime import date

from mta_od_data._raptor import Version, assign_date
from mta_od_data.downloads import od_parquet
from mta_od_data.platforms import DEFAULT_OUT as PLATFORMS
from mta_od_data.raptor import DEFAULT_CONFIG, DEFAULT_STATIONS, feed_for

day = date.fromisoformat(sys.argv[1])
assign_date(
    Version.open(feed_for(day)),
    day,
    od_parquet(),
    DEFAULT_STATIONS,
    PLATFORMS,
    DEFAULT_CONFIG,
    sys.argv[2],
    1,
)
EOF
)

echo "rebuilding as usual"
uv sync --quiet --reinstall-package mta-od-data
echo "wrote $out/dhat-heap.json"
