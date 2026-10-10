#!/usr/bin/env bash
# Profile the `raptor` extension's heap with `dhat` while it assigns one date.
#
# Usage: scripts/profile-heap.sh [--od <OD parquet>] [--date <date>] [--feed <zip>]
#
# Builds the extension with the `dhat-heap` feature (`dhat`'s allocator, not `mimalloc`),
# assigns the date, and writes `dhat-heap.json` to `~/.cache/mta-od-dhat/`,
# viewable in DHAT's viewer (https://nnethercote.github.io/dh_view/dh_view.html).
# Then rebuilds the extension as usual.
#
# `dhat` records every allocation's backtrace, so a full date takes many minutes:
# pass `--od` a sample (e.g. one in eight origins, as `scripts/build-pgo.sh` trains on).

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

od="$root/data/mta_od.parquet"
date=2025-10-15
feed="$root/data/gtfs/mdb-516-202510180014.zip"
while (($#)); do
    case "$1" in
        --od) od="$(realpath "$2")"; shift 2 ;;
        --date) date="$2"; shift 2 ;;
        --feed) feed="$(realpath "$2")"; shift 2 ;;
        *) echo "unknown argument $1" >&2; exit 1 ;;
    esac
done

# On disk, not in `/tmp` (tmpfs, RAM).
out="$HOME/.cache/mta-od-dhat"
mkdir -p "$out"

cd "$root"
echo "building with dhat"
MATURIN_PEP517_ARGS="--features dhat-heap" CARGO_PROFILE_RELEASE_DEBUG=line-tables-only \
    uv sync --quiet --reinstall-package mta-od-data

echo "assigning $date"
# `dhat` writes to the working directory.
(
    cd "$out"
    "$root/.venv/bin/mta-od-data" raptor assign \
        --feed "$feed" --date "$date" --od "$od" \
        --stations "$root/data/stations.csv" --config "$root/raptor/assign.json5" \
        --out "$out/paths.parquet" 2>&1 \
        | rg '^dhat:' || true
)

echo "rebuilding as usual"
uv sync --quiet --reinstall-package mta-od-data
echo "wrote $out/dhat-heap.json"
