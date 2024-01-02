from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from json import load
from src.misc.tools.common import get_plot_path, get_solution_path


class Chart:
    def __init__(self, solution: str) -> None:
        self.solution = solution
        self.workbook = Workbook()
        self.out = get_plot_path(solution)
        self.source = get_solution_path(solution)
        self.data = []

    def set_data(self) -> None:
        with open(self.source) as f:
            raw = load(f)
        if self.solution.lower() == "gda":
            self.data = [
                [data["iter"], data["score"]] for data in raw["paths"]["accepted"]
            ]
        elif self.solution.lower() == "hsa":
            self.data = [
                [data["iter"], data["score"]] for data in raw["paths"]["best_per_iter"]
            ]
        else:
            raise ValueError("Invalid solution set to Chart")

    def create_chart(self) -> None:
        headers = ["Iteration", "Distance"]
        data = self.data.copy()
        data.insert(0, headers)
        wb = self.workbook
        ws = wb.active
        for row in data:
            ws.append(row)  # type: ignore
        c1 = LineChart()
        c1.title = f"{self.solution.upper()} for TSP"
        c1.style = 13
        c1.x_axis.title = "Iteration"
        c1.y_axis.title = "Distance"

        data = Reference(ws, min_col=2, min_row=1, max_col=4, max_row=7)
        c1.add_data(data, titles_from_data=True)

        s1 = c1.series[0]
        s1.graphicalProperties.line.solidFill = "00AAAA"
        # s1.graphicalProperties.line.dashStyle = "sysDot"
        s1.graphicalProperties.line.width = 8800

        ws.add_chart(c1, "A10") # type: ignore

        wb.save(str(self.out))
