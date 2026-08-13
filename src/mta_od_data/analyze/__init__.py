from typer import Typer

from mta_od_data.analyze import one_seat_rides

app = Typer()
app.add_typer(one_seat_rides.app)
