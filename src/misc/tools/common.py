import math
import random
from pathlib import Path
from typing import Any
from networkx import Graph
from json import load, dump
from src.misc.validator import validate_schema


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def get_graph_conf_path() -> Path:
    return get_project_root() / "src" / "data" / "graph.json"


def get_solution_path(solution: str) -> Path:
    return get_project_root() / "src" / "data" / f"{solution}.json"


def get_plot_path(solution: str) -> Path:
    return get_project_root() / "out" / f"{solution}.xlsx"


def get_node_pairs(path: list[str]) -> list[tuple[str, str]]:
    """
    Generates non-repetitive node pairs from the given path list
    """
    node_pairs = []
    limit = len(path) - 1
    for i, node in enumerate(path):
        if i != limit:
            node_pairs.append((node, path[i + 1]))
    return node_pairs


def get_solution_score(g: Graph, solution: list) -> int:
    total = 0
    if type(solution[0]) == str:
        solution = get_node_pairs(solution)
    for node_pair in solution:
        edge = g.get_edge_data(node_pair[0], node_pair[1])
        total += edge["weight"]
    return total


def calculate_up(level: float, est_quality: int, max_iter: int) -> float:
    return (level - est_quality) / max_iter


def walker(G: Graph, start_idx: int, end_idx: int) -> list[str]:
    """
    Walks into each node of the graph exactly once from start to end node randomly
    """
    node_count = G.number_of_nodes()
    nodes = list(G)
    start = nodes[start_idx]
    end = nodes[end_idx]
    visited = [start]
    current = start
    while len(visited) < node_count:
        neighbors = [
            i for i in list(G.neighbors(current)) if (i not in visited and i != end)
        ]
        if len(neighbors) != 0:
            next = random.choice(neighbors)
            visited.append(next)
            current = next
        else:
            break
    visited.append(end)
    return visited


def swap(nodes: list[Any]) -> None:
    """
    Randomly swap nodes other than the first and last node
    """
    list_cp = nodes[1 : len(nodes) - 1]
    j, k = random.sample(range(len(list_cp)), 2)
    list_cp[j], list_cp[k] = list_cp[k], list_cp[j]
    nodes[1 : len(nodes) - 1] = list_cp


def estimate_quality(G: Graph, optimism: float) -> int:
    """
    Optimism is a number from 0 - 1
    """
    if optimism > 1 or optimism < 0:
        raise ValueError("Optimism value must be between 0 and 1")
    avg = get_avg_weight(G)
    node_count = G.number_of_nodes()
    est_total = avg * node_count
    return math.floor((1 - optimism / 2) * est_total)


def get_avg_weight(G: Graph) -> float:
    total = 0
    edges = G.edges(data=True)
    for edge in edges:
        total += edge[2]["weight"]
    return math.floor(total / G.number_of_edges())


def write_to_solution_json(data: dict, solution: str) -> None:
    fp = get_solution_path(solution)
    try:
        with open(fp, "w") as f:
            dump(data, f, indent=4)
    except:
        raise


def write_to_graph_json(nodes, w_nodes) -> None:
    p = get_graph_conf_path()
    with open(p, "r") as f:
        conf = load(f)
    conf["nodes"] = nodes
    conf["w_nodes"] = w_nodes
    with open(p, "w") as f:
        dump(conf, f, indent=4)
