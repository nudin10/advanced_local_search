import typer
from src.excel.plot import Chart
from src.misc.exceptions import GraphNotInitialisedError
from src.algorithm.hsa import run
from src.model.tsp import get_tsp_graph

app = typer.Typer(no_args_is_help=True)


@app.command(name="run")
def run_():
    try:
        G = get_tsp_graph()
    except GraphNotInitialisedError as err:
        raise
    run(G)


@app.command(name="plot")
def plot_():
    try:
        G = get_tsp_graph()
    except GraphNotInitialisedError as err:
        raise
    C = Chart("hsa")
    C.set_data()
    C.create_chart()
