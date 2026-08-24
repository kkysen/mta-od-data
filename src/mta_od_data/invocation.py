"""The command line a run was invoked with, as the reports quote it.

Every `analyze` report embeds a `Produced by` line, which the snapshot
tests then diff against a fresh run, so the line has to say exactly what
would reproduce the file. Read straight from `sys.argv` that's only true
of a real subprocess; read from the click context it's equally true of
`app(args=[...])` in the same process, which is what lets a test invoke
the CLI without assigning to `sys.argv` behind its own back.
"""

import shlex
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, override

from typer import Context
from typer.core import TyperGroup


class InvocationGroup(TyperGroup):
    """The root group, which stores its own command line as `ctx.obj`.

    `main` is the one place where click has both halves of an
    invocation, having just defaulted each to what the shell gave it,
    and it's above every command, so a nested context inherits the
    `obj` rather than each command reconstructing it.
    """

    @override
    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        # The same defaults click would apply, applied here so what's
        # recorded is what's about to be parsed.
        argv = sys.argv[1:] if args is None else list(args)
        # `Path(...).name`, not the full `sys.argv[0]`, since the report
        # quotes a command to retype rather than the path it ran from.
        prog = Path(sys.argv[0]).name if prog_name is None else prog_name
        # `setdefault`, so a caller with its own `obj` keeps it:
        # nothing passes one today, and this failing silently later
        # would be a `Produced by` line quoting the wrong command.
        extra.setdefault("obj", shlex.join([prog, *argv]))
        return super().main(
            args=argv,
            prog_name=prog,
            complete_var=complete_var,
            standalone_mode=standalone_mode,
            windows_expand_args=windows_expand_args,
            **extra,
        )


def produced_by(ctx: Context) -> str:
    """The command line `ctx` was invoked with.

    An `assert` rather than a fallback to `sys.argv`: a missing `obj`
    means the command was reached without `InvocationGroup.main`, and a
    fallback would paper over that with a plausible-looking line that
    can be wrong in exactly the case the tests exist to catch.
    """
    invocation = ctx.obj
    assert isinstance(invocation, str), (
        f"no invocation recorded on the context ({invocation!r}): "
        f"the root app must use `cls=InvocationGroup`"
    )
    return invocation
