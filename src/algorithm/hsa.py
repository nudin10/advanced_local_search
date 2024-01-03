# Author: Ahmad Nuruddin bin Azhar
from random import randint
from src.model.tsp import TspGraph
from src.model.hsa import HSA, TSP_Solution
from src.misc.tools.common import write_to_solution_json, swap


def run(G: TspGraph):
    # --- SETUP ---
    all_sols: list[TSP_Solution] = []
    best_sols: list[TSP_Solution] = []
    accepted_sols: list[TSP_Solution] = []
    # --- SETUP ---

    # --- INITIALIZATION ---
    hsa = HSA(G)
    hsa.hms = 5
    hsa.hcmr = 0.7
    hsa.pitch_adjust_rate = 0.2
    hsa.number_of_improvisation = 500
    hsa.init_hm(G)
    # --- INITIALIZATION ---

    # --- IMPROVEMENT PHASE --
    i = 1
    while i <= hsa.number_of_improvisation:
        if randint(0, 1) < hsa.hcmr:
            sol: TSP_Solution = TSP_Solution(G)
            sol.iter = i
            sol.path = hsa.select_member().path.copy()
            if randint(0, 1) < hsa.pitch_adjust_rate:
                swap(sol.path)
            sol.calculate_solution()
            all_sols.append(sol)
            worst_sol = max(hsa.hm)
            if sol.score < worst_sol.score:
                if sol not in accepted_sols:
                    accepted_sols.append(sol)
                hsa.hm[hsa.hm.index(worst_sol)] = sol
                if sol not in best_sols:
                    best_sols.append(min(hsa.hm))
        i += 1
    best_sol = min(hsa.hm)
    # --- IMPROVEMENT PHASE --

    # --- OUTPUT ---
    data = {
        "name": "HSA data",
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
        },
    }
    write_to_solution_json(data, "hsa")
    # --- OUTPUT ---


def reset():
    data = {
        "name": "HSA data",
        "paths": {
            "all": [{"path": [], "score": [], "iter": []}],
            "accepted": [{"path": [], "score": [], "iter": []}],
            "best": {"path": [], "score": [], "iter": []},
            "best_per_iter": [{"path": [], "score": [], "iter": []}],
        },
    }
    write_to_solution_json(data, "hsa")
