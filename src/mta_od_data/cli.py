from typer import Typer

from mta_od_data import analyze, prepare_data

app = Typer(rich_markup_mode=None)
app.command("prepare")(prepare_data.main)

analyze_app = Typer(rich_markup_mode=None)
analyze_app.command("one-seat-rides")(analyze.main)
app.add_typer(analyze_app, name="analyze")
