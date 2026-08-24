"""The command line a run was invoked with, as the reports quote it.

Every `analyze` report embeds a `Produced by` line, which the snapshot
tests then diff against a fresh run, so the line has to say exactly what
would reproduce the file. Read straight from `sys.argv` that's only true
of a real subprocess; read from the click context it's equally true of
`app(args=[...])` in the same process, which is what lets a test invoke
the CLI without assigning to `sys.argv` behind its own back.
"""

import shlex
from dataclasses import dataclass
from typing import Any, override

from typer import Context
from typer._click.core import Context as ClickContext
from typer.core import TyperGroup


@dataclass(frozen=True, slots=True)
class Invocation:
    info_name: str
    args: tuple[str, ...]

    @override
    def __str__(self) -> str:
        return shlex.join((self.info_name, *self.args))


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

    # `ClickContext`, not the `Context` a command is handed: the base
    # `make_context` is declared in terms of the click class typer
    # vendors, and `typer.Context` is a subclass of it, which would
    # narrow a parameter the base declares wider. It has no public name,
    # hence the private import.
    @override
    def make_context(
        self,
        info_name: str | None,
        args: list[str],
        parent: ClickContext | None = None,
        **extra: Any,
    ) -> ClickContext:
        # `main` always resolves a program name before it gets here,
        # and this group is only ever the root, so a `None` is a caller
        # that bypassed `main` rather than a run to record.
        assert info_name is not None, "the root group is invoked by name"
        # Before `super()`, which parses `args` and is free to consume it.
        extra["obj"] = Invocation(info_name=info_name, args=tuple(args))
        return super().make_context(info_name, args, parent=parent, **extra)


def produced_by(ctx: Context) -> Invocation:
    """The command line `ctx` was invoked with.

    An `assert` rather than a fallback to `sys.argv`: a missing `obj`
    means the command was reached without `InvocationGroup`, and a
    fallback would paper over that with a plausible-looking line that
    can be wrong in exactly the case the tests exist to catch.
    """
    invocation = ctx.obj
    assert isinstance(invocation, Invocation), (
        f"no invocation recorded on the context ({invocation!r}): "
        f"the root app must use `cls=InvocationGroup`"
    )
    return invocation
