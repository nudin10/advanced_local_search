from typing import Annotated
import typer
from src.misc.exceptions import GraphNotInitialisedError
from src.model.tsp import init_graph, show_graph, reset_graph

app = typer.Typer(no_args_is_help=True)

@app.command(
    name="init", 
    help="Initialise TSP graph",
)
def init_graph_(
    min: Annotated[
        int,
        typer.Argument(show_default=False, help="Provide minimum graph node number to seed to randomiser")
    ],
    max: Annotated[
        int,
        typer.Argument(show_default=False, help="Provide maximum graph node number to seed to randomiser")
    ],
):
    try:
        init_graph(min, max)
    except GraphNotInitialisedError:
        raise

@app.command(
    name="show", 
    help="Shows TSP graph",
)
def show_graph_():
    try:
        show_graph()
    except GraphNotInitialisedError:
        raise

# @app.command(
#     name="reset", 
#     help="Resets TSP graph",
# )
# def reset_graph_():
#     reset_graph()

# @app.command()
# def init_