from pathlib import Path

# Relative to the actual invocation directory rather than absolute: computed
# once, at import time, as the (possibly ../-prefixed) offset from cwd back
# to the real project root, so it round-trips correctly through any later
# file I/O in this process regardless of where the CLI was invoked from --
# verified directly (`mta-od-data prepare` and the pytest suite both still
# find the real files when run from an unrelated cwd via `uv run --project`).
# Relies on cwd staying fixed for the process's lifetime, which nothing here
# violates. Being relative also means every default path derived from it is
# naturally short in --help, with no separate show_default handling needed.
ROOT = (
    Path(__file__).resolve().parent.parent.parent.relative_to(Path.cwd(), walk_up=True)
)
DATA = ROOT / "data"
