from typer import Typer

from mta_od_data import analyze, gtfs, prepare
from mta_od_data.invocation import InvocationGroup

app = Typer(cls=InvocationGroup)
app.add_typer(prepare.app)
app.add_typer(gtfs.app)
app.add_typer(analyze.app, name="analyze")
