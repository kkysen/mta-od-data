from pathlib import Path

# Relative to cwd rather than absolute, so every default path derived from
# it stays short in --help. Computed once at import, and relies on cwd
# staying put for the process's lifetime, which nothing here violates.
ROOT = (
    Path(__file__).resolve().parent.parent.parent.relative_to(Path.cwd(), walk_up=True)
)
DATA = ROOT / "data"
