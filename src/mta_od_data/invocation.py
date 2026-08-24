"""The command line a run was invoked with, as the reports quote it.

Every `analyze` report embeds a `Produced by` line, which the snapshot
tests then diff against a fresh run, so the line has to say exactly what
would reproduce the file. Read straight from `sys.argv` that's only true
of a real subprocess; read from the click context it's equally true of
`app(args=[...])` in the same process, which is what lets a test invoke
the CLI without assigning to `sys.argv` behind its own back.
"""

import shlex
from typing import Any, override

from typer import Context
from typer.core import TyperGroup


class InvocationGroup(TyperGroup):
    """The root group, which stores its own command line as `ctx.obj`.

    `make_context` rather than `main`, though `main` is where the two
    halves of an invocation arrive: `main` is also where click defaults
    each of them, from `sys.argv` and from `_detect_program_name`, and
    it hands the results to `make_context`. Recording them here is
    therefore recording what click resolved and is about to parse,
    without this having to re-derive either and drift from it.

    The root group only, so a nested context inherits the `obj` rather
    than each command reconstructing it: click builds a subcommand's
    context with that subcommand's own class.
    """

    # `parent` and the return are the click `Context` that typer vendors
    # as `typer._click.core`, a base of the public `typer.Context` and
    # not exported anywhere public itself. `Any` rather than reaching
    # into a private module for a name that only appears in a signature
    # this never looks at.
    @override
    def make_context(
        self,
        info_name: str | None,
        args: list[str],
        parent: Any = None,
        **extra: Any,
    ) -> Any:
        # `main` always resolves a program name before it gets here,
        # and this group is only ever the root, so a `None` is a caller
        # that bypassed `main` rather than a run to record.
        assert info_name is not None, "the root group is invoked by name"
        # Before `super()`, which parses `args` and is free to consume
        # it, and `setdefault` so a caller with its own `obj` keeps it:
        # nothing passes one today, and this quietly losing to one later
        # would be a `Produced by` line quoting the wrong command.
        extra.setdefault("obj", shlex.join([info_name, *args]))
        return super().make_context(info_name, args, parent=parent, **extra)


def produced_by(ctx: Context) -> str:
    """The command line `ctx` was invoked with.

    An `assert` rather than a fallback to `sys.argv`: a missing `obj`
    means the command was reached without `InvocationGroup`, and a
    fallback would paper over that with a plausible-looking line that
    can be wrong in exactly the case the tests exist to catch.
    """
    invocation = ctx.obj
    assert isinstance(invocation, str), (
        f"no invocation recorded on the context ({invocation!r}): "
        f"the root app must use `cls=InvocationGroup`"
    )
    return invocation
