"""
--- Day 11: Cosmic Expansion ---
https://adventofcode.com/2023/day/11
"""
import collections
from itertools import combinations

from utils.test_and_run import run, test
from utils.pathfinding import manhattan_distance

EMPTY = "."
GALAXY = "#"


class CosmicExpansion:
    def __init__(self, inp):
        self._inp = inp

        self.height = len(self._inp)
        self.width = len(self._inp[0])

        self._universe = self._expand()
        self._galaxies = list(self._get_galaxies_positions())
        self._galaxy_pairs = combinations(self._galaxies, 2)

    def _expand(self):
        universe = [list(line) for line in self._inp]
        rows_to_expand = []
        cols_to_expand = []
        for i, line in enumerate(self._inp):
            if all([s == EMPTY for s in line]):
                rows_to_expand.append(i)

        for col_idx in range(self.width):
            col = [line[col_idx] for line in self._inp]
            if all([s == EMPTY for s in col]):
                cols_to_expand.append(col_idx)

        for i, row_idx in enumerate(rows_to_expand):
            universe.insert(i + row_idx, list(self._inp[row_idx]))

        for i, col_idx in enumerate(cols_to_expand):
            for line in universe:
                line.insert(i + col_idx, EMPTY)

        return universe

    def _get_galaxies_positions(self):
        for y, row in enumerate(self._universe):
            for x, elm in enumerate(row):
                if elm == GALAXY:
                    yield x, y

    def get_galaxy_shortest_path_sum(self):
        res = 0
        for pair in self._galaxy_pairs:
            distance = manhattan_distance(*pair)
            res += distance
        return res


def cosmic_expansion(inp, part=1, **kw):
    if part == 2:
        raise NotImplemented
    return CosmicExpansion(inp).get_galaxy_shortest_path_sum()


if __name__ == "__main__":
    test(cosmic_expansion, 374)
    run(cosmic_expansion)
