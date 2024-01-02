import typer
from app.commands import gda, hsa, tsp

app = typer.Typer(help="A simple CLI program to demonstrate Great Deluge Algorithm and Harmony Search Algorithm", no_args_is_help=True)

app.add_typer(
    tsp.app,
    name="graph",
    help="Initialise, reset or show graph"
)

app.add_typer(
    gda.app,
    name="gda",
    help="Great Deluge Algorithm"
)

app.add_typer(
    hsa.app,
    name="hsa",
    help="Harmony Search Algorithm"
)