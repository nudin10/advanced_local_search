# Author: Ahmad Nuruddin bin Azhar
from src.model.gda import GD_Solution
from src.model.tsp import TspGraph
from src.misc.tools.common import (
    calculate_up,
    estimate_quality,
    swap,
    walker,
    write_to_solution_json,
)
from rich import print
from src.model.tsp import TspGraph


def run(G: TspGraph):
    # --- SETUP ---
    est_quality = estimate_quality(G.get_graph(), 0.6)
    # print(est_quality)
    max_iter = 50
    all_sols: list[GD_Solution] = []
    best_sol = GD_Solution(G)
    best_sol.path = []
    accepted_sols: list[GD_Solution] = []
    # --- SETUP ---

    # --- INITIALIZATION ---
    init_sol = GD_Solution(G)
    init_sol.iter = 0
    init_sol.path = walker(G.get_graph(), 0, 0)
    init_sol.calculate_score()
    all_sols.append(init_sol)
    best_sol.path = init_sol.path
    best_sol.calculate_score()
    level = best_sol.score
    up = calculate_up(level, est_quality, max_iter)
    path = init_sol.path.copy()
    # --- INITIALIZATION ---

    # --- IMPROVEMENT PHASE --
    i = 1
    while i <= max_iter:
        p = path.copy()
        swap(p)
        sol = GD_Solution(G)
        sol.iter = i
        sol.path = p
        sol.calculate_score()
        all_sols.append(sol)

        if sol.score < level:
            if p not in accepted_sols:
                accepted_sols.append(sol)
            up = calculate_up(level, est_quality, max_iter)
            level = level - up
            if sol.score < best_sol.score:
                best_sol = sol
            path = p

        i += 1
    # --- IMPROVEMENT PHASE --
        
    # --- OUTPUT ---
    data = {
        "name": "GDA data",
        "paths": {
            "all": [{"path": sol.path, "score": sol.score, "iter": sol.iter} for sol in all_sols],
            "accepted": [{"path": sol.path, "score": sol.score, "iter": sol.iter} for sol in accepted_sols],
            "best": {"path": best_sol.path, "score": best_sol.score, "iter": best_sol.iter},
        },
    }
    write_to_solution_json(data, "gda")
    # --- OUTPUT ---
