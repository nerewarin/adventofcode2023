"""
--- Day 19: Aplenty  ---
https://adventofcode.com/2023/day/19
"""

from utils.input_formatters import cast_2d_list_elements
from utils.pathfinding import manhattan_distance, aStarSearch
from utils.position_search_problem import PositionSearchProblem
from utils.test_and_run import run, test


class Aplenty:
    def __init__(self, inp):
        self.raw_inp = inp
        self.inp = self._parse_input(inp)

    @staticmethod
    def _parse_input(inp):
        return [Brick.from_line(line, line_num) for line_num, line in enumerate(inp)]

    def get_sum_of_ratings(self):
        return 0


def aplenty(inp, **kw):
    return Aplenty(inp).get_sum_of_ratings()


if __name__ == "__main__":
    test(aplenty, 19114)
    res = run(aplenty)
