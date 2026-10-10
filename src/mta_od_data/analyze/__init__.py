from typer import Typer

from mta_od_data.analyze import (
    deinterlining,
    line_ridership,
    one_seat_rides,
    regional_flow,
    track_ridership,
)

app = Typer()
app.add_typer(one_seat_rides.app)
app.add_typer(regional_flow.app)
app.add_typer(deinterlining.app)
app.add_typer(track_ridership.app)
app.add_typer(line_ridership.app)
