from src.model.tsp import TspGraph
from src.misc.tools.common import get_solution_score


class GD_Solution:
    def __init__(self, G: TspGraph) -> None:
        self._G = G.get_graph()
        self.iter = 0
        self.path = []
        self.score = 0
        self.level = 0
        self.up = 0

    def __eq__(self, compare) -> bool:
        return isinstance(compare, GD_Solution) and compare.path == self.path

    def __ne__(self, compare) -> bool:
        return isinstance(compare, GD_Solution) and compare.path != self.path
    
    def __str__(self) -> str:
        return f"Path: {self.path}, Score: {self.score}, Iter: {self.iter}"

    def calculate_score(self) -> None:
        if len(self.path) == 0:
            self.score = 0
        else:
            self.score = get_solution_score(self._G, self.path)
