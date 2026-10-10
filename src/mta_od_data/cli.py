from typer import Typer

from mta_od_data import analyze, gtfs, prepare, raptor, scale_od
from mta_od_data.invocation import InvocationGroup

app = Typer(cls=InvocationGroup)
app.add_typer(prepare.app)
app.add_typer(gtfs.app)
app.add_typer(scale_od.app)
app.add_typer(raptor.app, name="raptor")
app.add_typer(analyze.app, name="analyze")
