"""
--- Day 12: Hot Springs ---
https://adventofcode.com/2023/day/12
"""
from itertools import combinations

from utils.test_and_run import run, test
from utils.pathfinding import manhattan_distance

EMPTY = "."
GALAXY = "#"


class CosmicExpansion:
    def __init__(self, inp, expansion_rate):
        self._inp = inp
        self._expansion_rate = expansion_rate

        self.height = len(self._inp)
        self.width = len(self._inp[0])

        self._universe, self._rows_to_expand, self._cols_to_expand = self._expand()
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

        return universe, rows_to_expand, cols_to_expand

    def _get_galaxies_positions(self):
        for y, row in enumerate(self._universe):
            for x, elm in enumerate(row):
                if elm == GALAXY:
                    yield x, y

    def get_galaxy_shortest_path_sum(self):
        print("     ", "  ".join(["  v" if x in self._cols_to_expand else "   " for x in range(len(self._inp))]))
        print("     ", "  ".join(list(f"{x: 3}" for x in range(len(self._inp)))))
        for i, line in enumerate(self._inp):
            suff = " "
            pref = " "
            if i in self._rows_to_expand:
                suff = "<"
                pref = ">"
            print(f"{pref} {i: 3} {list(line)} {suff}")
        print()

        res = 0
        for pair in self._galaxy_pairs:
            p1, p2 = pair

            x1, y1 = p1
            x2, y2 = p2

            xl, yl = min(x2, x1), min(y2, y1)
            xh, yh = max(x2, x1), max(y2, y1)

            base_dist = manhattan_distance(*pair)

            empty_rows = 0
            for empty_row in self._rows_to_expand:
                if yl <= empty_row <= yh:
                    empty_rows += 1

            empty_cols = 0
            for empty_col in self._cols_to_expand:
                if xl <= empty_col <= xh:
                    empty_cols += 1

            distance = base_dist + (self._expansion_rate - 1) * (empty_rows + empty_cols)
            print(f"{pair=} distance = {base_dist} + {str(self._expansion_rate - 1)} * ({empty_rows=} + {empty_cols=}) = {distance}")

            res += distance
        return res


def hot_springs(inp, part=1, expansion_rate=None, **kw):
    if expansion_rate is None:
        if part == 1:
            expansion_rate = 2
        elif part == 2:
            expansion_rate = 1000000

    return CosmicExpansion(inp, expansion_rate).get_galaxy_shortest_path_sum()


if __name__ == "__main__":
    test(hot_springs, 21)
    run(hot_springs)

