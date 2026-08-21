"""Markdown table syntax, kept apart from what the tables say.

Deliberately not `tabulate` or another table library:
they pad every cell to its column's width,
and a committed report repadded because one number gained a digit
is a diff the size of the table for a change the size of a digit.
See `table_rule` for the rest of that argument.
"""


def table_rule(alignments: str) -> str:
    """A markdown table's header rule, `l`/`r` per column.

    Right-aligned numeric columns so a reader can compare magnitudes
    down a column at a glance.
    Alignment markers only, not padding:
    a rendered table lines up either way,
    while padding the source to the widest cell
    means one number gaining a digit repads its whole column
    and every row of a committed report shows as changed.
    """
    cells = {"l": " --- ", "r": " ---: "}
    return "|" + "|".join(cells[a] for a in alignments) + "|"


def table_row(*cells: str) -> str:
    """One markdown table row, `| |` for an empty cell.

    Not `|  |`: a cell padded on both sides of nothing
    is trailing whitespace, which markdown linters flag.
    """
    return "|" + "|".join(f" {cell} " if cell else " " for cell in cells) + "|"
