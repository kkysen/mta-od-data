"""SVG bar charts of the `ridership` reports' tables:
each a measure's rows ranked, as horizontal bars, one series per riders column.

Each chart is drawn from its report's own table,
so every bar is labelled with exactly the number its row shows,
and is a standalone SVG with its own light and dark colors,
so it reads the same embedded in a Markdown report on GitHub or opened alone.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from html import escape
from math import ceil, floor, log10

# Categorical slots 1 and 2 (blue, orange), validated for both modes
# (`dataviz` skill's `validate_palette.js`): light, then dark.
SERIES = [("#2a78d6", "#3987e5"), ("#eb6834", "#d95926")]

WIDTH = 760
# The least a chart's bars get, however long its labels: it widens instead.
MIN_PLOT_W = 480
FONT = 12
# An average glyph's width at `FONT`, for sizing the label column.
CHAR_W = 6.6
BAR_H = 12
BAR_GAP = 2
ROW_GAP = 8
PAD = 16
TITLE_H = 48
AXIS_H = 24
LEGEND_H = 24

STYLE = """
svg { --bg:#fcfcfb; --ink:#0b0b0b; --ink2:#52514e; --grid:#e4e3df; %(light)s }
@media (prefers-color-scheme: dark) {
  svg { --bg:#1a1a19; --ink:#f0efec; --ink2:#c3c2b7; --grid:#3a3936; %(dark)s }
}
text {
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size: %(font)spx;
  fill: var(--ink2);
}
.title { font-size: 15px; font-weight: 600; fill: var(--ink); }
.label { fill: var(--ink); }
.grid { stroke: var(--grid); stroke-width: 1; }
%(series)s
"""


@dataclass(frozen=True, slots=True)
class Bar:
    """A row's bars: each series' value, and its text as the table shows it."""

    label: str
    values: Sequence[float | None]
    texts: Sequence[str]


@dataclass(frozen=True, slots=True)
class Chart:
    """A chart of a table's rows: `columns`' values, one series each,
    named in its legend as `series`, ranked by the first."""

    slug: str
    title: str
    columns: Sequence[str]
    series: Sequence[str]
    note: str = ""
    # A row's label from its cells by their column's heading,
    # if not its first `keys` cells.
    label: Callable[[Mapping[str, str]], str] | None = None


def cells(row: str) -> list[str]:
    """A `table_row`'s cells."""
    return [c.strip() for c in row.strip()[1:-1].split("|")]


def number(text: str) -> float | None:
    return float(text.replace(",", "")) if text else None


def first_value(bar: Bar) -> float:
    return bar.values[0] or 0.0


def table_charts(
    table: Sequence[str], keys: int, subtitle: str, charts: Sequence[Chart]
) -> dict[str, str]:
    """Each of `charts` of a report's `table`, by its slug, as an SVG:
    its rows labelled by their first `keys` cells, and ranked."""
    head = cells(table[0])
    rows = [cells(r) for r in table[2:] if r.startswith("|")]
    out: dict[str, str] = {}
    for c in charts:
        idx = [head.index(col) for col in c.columns]
        bars: list[Bar] = [
            Bar(
                c.label(dict(zip(head, r, strict=True)))
                if c.label
                else ": ".join(r[:keys]),
                [number(r[i]) for i in idx],
                [r[i] for i in idx],
            )
            for r in rows
            if r[idx[0]]
        ]
        bars.sort(key=first_value, reverse=True)
        sub = f"{subtitle}; {c.note}" if c.note else subtitle
        out[c.slug] = bar_chart(c.title, sub, c.series, bars)
    return out


def nice_ticks(top: float) -> list[float]:
    """Round ticks from 0 to past `top`, about 5 of them."""
    if top <= 0:
        return [0.0, 1.0]
    raw = top / 5
    mag = 10 ** floor(log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return [i * step for i in range(ceil(top / step) + 1)]


def style() -> str:
    return STYLE % {
        "light": "".join(f"--s{i}:{c[0]};" for i, c in enumerate(SERIES)),
        "dark": "".join(f"--s{i}:{c[1]};" for i, c in enumerate(SERIES)),
        "font": FONT,
        "series": "\n".join(f".s{i} {{ fill: var(--s{i}); }}" for i in range(2)),
    }


def bar_path(x: float, y: float, w: float, h: float, r: float = 4) -> str:
    """A bar from the baseline at `x`, its data end rounded."""
    r = min(r, w, h / 2)
    return (
        f"M{x:.1f},{y:.1f}h{w - r:.1f}a{r},{r} 0 0 1 {r},{r}"
        f"v{h - 2 * r:.1f}a{r},{r} 0 0 1 {-r},{r}h{-(w - r):.1f}z"
    )


def text(x: float, y: float, s: str, attrs: str = "") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}"{attrs}>{escape(s)}</text>'


def bar_chart(
    title: str, subtitle: str, series: Sequence[str], bars: Sequence[Bar]
) -> str:
    """Horizontal bars, one row per `bars`, in its order, one bar per `series`,
    each labelled with its text."""
    n = len(series)
    label_w = max(len(b.label) for b in bars) * CHAR_W + 8
    value_w = max(len(t) for b in bars for t in b.texts) * CHAR_W
    plot_x = PAD + label_w
    width = max(WIDTH, plot_x + MIN_PLOT_W + value_w + 6 + PAD)
    plot_w = width - plot_x - PAD - value_w - 6
    row_h = n * BAR_H + (n - 1) * BAR_GAP
    top = PAD + TITLE_H + (LEGEND_H if n > 1 else 0)
    bottom = top + len(bars) * (row_h + ROW_GAP)
    height = bottom + AXIS_H + PAD
    vmax = max((v for b in bars for v in b.values if v is not None), default=0)
    ticks = nice_ticks(vmax)
    scale = plot_w / ticks[-1]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" '
        f'height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}" '
        f'role="img" aria-label="{escape(title)}">',
        f"<style>{style()}</style>",
        '<rect width="100%" height="100%" fill="var(--bg)"/>',
        text(PAD, PAD + 15, title, ' class="title"'),
        text(PAD, PAD + 35, subtitle),
    ]
    x = PAD
    for i, s in enumerate(series if n > 1 else []):
        y = PAD + TITLE_H
        out.append(
            f'<rect class="s{i}" x="{x}" y="{y}" width="12" height="12" rx="2"/>'
        )
        out.append(text(x + 18, y + 10, s))
        x += 18 + len(s) * CHAR_W + 20
    for t in ticks:
        x = plot_x + t * scale
        out.append(
            f'<line class="grid" x1="{x:.1f}" x2="{x:.1f}" '
            f'y1="{top - 4}" y2="{bottom}"/>'
        )
        out.append(text(x, bottom + 16, f"{t:,g}", ' text-anchor="middle"'))
    for r, b in enumerate(bars):
        y0 = top + r * (row_h + ROW_GAP) + ROW_GAP / 2
        out.append(
            text(
                plot_x - 8,
                y0 + row_h / 2 + 4,
                b.label,
                ' class="label" text-anchor="end"',
            )
        )
        for i, v in enumerate(b.values):
            if v is None:
                continue
            y = y0 + i * (BAR_H + BAR_GAP)
            w = max(v * scale, 1)
            tip = escape(f"{b.label}, {series[i]}: {b.texts[i]}")
            out.append(
                f'<path class="s{i}" d="{bar_path(plot_x, y, w, BAR_H)}">'
                f"<title>{tip}</title></path>"
            )
            out.append(text(plot_x + w + 4, y + BAR_H - 2, b.texts[i]))
    out.append("</svg>")
    return "\n".join(out) + "\n"
