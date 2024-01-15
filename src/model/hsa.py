from src.model.tsp import TspGraph
from random import choice, seed
from src.misc.tools.common import walker, get_solution_score
from rich import print


class TSP_Solution:
    def __init__(self, G: TspGraph) -> None:
        self._G = G.get_graph()
        self.iter = 0
        self.path: list[str] = []
        self.score = 0

    def __str__(self) -> str:
        return f"Path: {self.path}, Score: {self.score}, Iter: {self.iter}"

    def __eq__(self, compare):
        return isinstance(compare, TSP_Solution) and compare.path == self.path

    def __ne__(self, compare: object) -> bool:
        return isinstance(compare, TSP_Solution) and compare.path != self.path

    def __lt__(self, compare):
        return isinstance(compare, TSP_Solution) and self.score < compare.score

    def calculate_solution(self):
        if len(self.path) == 0:
            self.score = 0
        else:
            self.score = get_solution_score(self._G, self.path)
        return


class HSA:
    def __init__(self, G: TspGraph) -> None:
        self._G = G.get_graph()
        self.nodes = []
        self.hm: list[TSP_Solution] = []
        self.hms = 0
        self.hcmr: float = 0.00
        self.mem_size = 0
        self.mem_considering_rate = 0
        self.pitch_adjust_rate: float = 0.00
        self.number_of_improvisation: int = 0

    def init_hm(self, G: TspGraph) -> None:
        """
        Populates harmony memory with random solutions
        """
        if self.hms == 0:
            print("HMS is still set to 0!")
            return
        i = 0
        while i < self.hms:
            sol = TSP_Solution(G)
            # regenerate solution if duplicate
            while True:
                sol.path = walker(self._G, 0, 0)
                self.nodes = sol.path
                if sol not in self.hm:
                    sol.calculate_solution()
                    break
            self.hm.append(sol)
            i += 1

    def select_member(self) -> TSP_Solution:
        """
        Randomly select member solution from harmony memory
        """
        if len(self.hm) == 0:
            raise ValueError("No members to be selected!")
        return choice(self.hm)
