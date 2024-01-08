# Author: Ahmad Nuruddin bin Azhar
from src.model.gda import GD_Solution
from src.model.tsp import TspGraph
from src.misc.tools.common import (
    calculate_up,
    # estimate_quality,
    swap,
    walker,
    write_to_solution_json,
)
from src.model.tsp import TspGraph


def run(G: TspGraph):
    # --- SETUP ---
    est_quality = 100
    max_iter = 50
    all_sols: list[GD_Solution] = []
    best_sol = GD_Solution(G)
    best_sol.path = []
    accepted_sols: list[GD_Solution] = []
    best_sols: list[GD_Solution] = []
    p = []
    # --- SETUP ---

    # --- INITIALIZATION ---
    init_sol = GD_Solution(G)
    init_sol.iter = 0
    init_sol.path = walker(G.get_graph(), 0, 0)
    init_sol.calculate_score()
    prev_sol = init_sol
    best_sol.path = init_sol.path
    best_sol.calculate_score()
    level = best_sol.score
    init_sol.level = level
    all_sols.append(init_sol)
    up = calculate_up(level, est_quality, max_iter)
    # --- INITIALIZATION ---

    # --- IMPROVEMENT PHASE --
    i = 1
    while i <= max_iter:
        sol = GD_Solution(G)
        sol.iter = i
        if i == 1:
            p = swap(init_sol.path.copy())
            sol.level = level
        else:
            p = prev_sol.path.copy()
        p = swap(p)
        sol.path = p
        sol.calculate_score()
        if sol.score < best_sol.score:
            best_sol = sol
            prev_sol = sol
        if sol.score < level:
            accepted_sols.append(sol)
        all_sols.append(sol)
        best_sols.append(best_sol)
        print(sol)
        level -= up
        sol.level = level
        i += 1

        # for sol in all_sols:
        #     print(sol)
        # for sol in accepted_sols:
        #     print(sol)

        # for sol in best_sols:
        #     print(sol)
    # --- OUTPUT ---
    data = {
        "name": "GDA data",
        "paths": {
            "all": [
                {"path": sol.path, "score": sol.score, "iter": sol.iter}
                for sol in all_sols
            ],
            "accepted": [
                {"path": sol.path, "score": sol.score, "iter": sol.iter}
                for sol in accepted_sols
            ],
            "best": {
                "path": best_sol.path,
                "score": best_sol.score,
                "iter": best_sol.iter,
            },
                        "best_per_iter": [
                {"path": sol.path, "score": sol.score, "iter": sol.iter}
                for sol in best_sols
            ],
            "levels": [
                {"level": sol.level, "iter": sol.iter}
                for sol in all_sols
            ],
        },
    }
    write_to_solution_json(data, "gda")
    # --- OUTPUT ---


def reset():
    data = {
        "name": "GDA data",
        "paths": {
            "all": [{"path": [], "score": [], "iter": []}],
            "accepted": [{"path": [], "score": [], "iter": []}],
            "best": {"path": [], "score": [], "iter": []},
            "levels": []
        },
    }
    write_to_solution_json(data, "gda")
