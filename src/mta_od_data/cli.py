from typer import Typer

from mta_od_data import analyze, prepare_data

app = Typer(rich_markup_mode=None)
app.command("prepare-data")(prepare_data.main)
app.command("one-seat-rides")(analyze.main)
