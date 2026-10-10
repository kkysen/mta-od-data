#!/usr/bin/env bash
# Build the `raptor` extension with profile-guided optimization,
# for when many `raptor assign` runs make the slower build worth it.
#
# Builds an instrumented extension, assigns a sample of one date's OD rows with it
# (one in eight origins, so it takes seconds),
# merges the profile, and rebuilds the extension with it.
# On another sample, the result runs ~10% fewer cycles than a plain release build.
#
# Needs `llvm-profdata`: `rustup component add llvm-tools`.
# The next plain `uv sync` that rebuilds the extension undoes this.

set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$root"

# A date the feed covers, and its OD rows.
date=2025-09-16
feed=data/gtfs/mdb-516-202510180014.zip
od=data/mta_od.parquet

# `$RUSTFLAGS` replaces `.cargo/config.toml`'s flags rather than adding to them.
native="-C target-cpu=native"

sysroot="$(rustc --print sysroot)"
profdata="$(fd --type executable '^llvm-profdata$' "$sysroot" | head -n 1)"
if [[ -z "$profdata" ]]; then
    echo "no llvm-profdata: rustup component add llvm-tools" >&2
    exit 1
fi

# On disk, not in `/tmp` (tmpfs, RAM).
work="$HOME/.cache/mta-od-pgo"
rm -rf "$work"
mkdir -p "$work/profiles"

echo "writing a training sample of $date's OD rows"
uv run --no-sync python - "$od" "$date" "$work/od.parquet" <<'EOF'
import sys
from datetime import date

import duckdb

od, day, out = sys.argv[1], date.fromisoformat(sys.argv[2]), sys.argv[3]
duckdb.execute(
    """
    COPY (
        FROM read_parquet($od)
        WHERE Year = $year AND Month = $month AND "Day of Week" = $dow
            AND "Origin Station Complex ID" % 8 = 3
    ) TO $out (FORMAT parquet, COMPRESSION zstd)
    """,
    {"od": od, "year": day.year, "month": day.month, "dow": f"{day:%A}", "out": out},
)
EOF

echo "building the instrumented extension"
RUSTFLAGS="$native -C profile-generate=$work/profiles" \
    uv sync --quiet --reinstall-package mta-od-data

echo "training on the sample"
.venv/bin/mta-od-data raptor assign \
    --feed "$feed" --date "$date" --od "$work/od.parquet" --out "$work/paths.parquet" \
    > /dev/null

"$profdata" merge -o "$work/merged.profdata" "$work/profiles"

echo "building with the profile"
RUSTFLAGS="$native -C profile-use=$work/merged.profdata" \
    uv sync --quiet --reinstall-package mta-od-data

echo "built with PGO; a plain \`uv sync\` that rebuilds the extension undoes this"
