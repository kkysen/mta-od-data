from typer import Typer

from mta_od_data import analyze, prepare

app = Typer()
app.add_typer(prepare.app)
app.add_typer(analyze.app, name="analyze")
