from typer import Typer

from mta_od_data.analyze import (
    deinterlining,
    one_seat_rides,
    regional_flow,
    track_ridership,
)

app = Typer()
app.add_typer(one_seat_rides.app)
app.add_typer(regional_flow.app)
app.add_typer(deinterlining.app)
app.add_typer(track_ridership.app)
