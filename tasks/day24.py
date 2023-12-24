"""
--- Day 24: Never Tell Me The Odds ---
https://adventofcode.com/2023/day/24
"""
import collections
import dataclasses
from collections import defaultdict
from itertools import combinations

from utils.input_formatters import cast_2d_list_elements
from utils.position_search_problem import PositionSearchProblem
from utils.test_and_run import run, test


@dataclasses.dataclass
class Hailstone:
    position: tuple[int]
    velocity: tuple[int]
    name: str

    def __post_init__(self):
        self.x, self.y, self.z = self.position
        self.vx, self.vy, self.vz = self.velocity

    @classmethod
    def from_line(cls, line, line_num):
        return cls(*(tuple(int(s) for s in side.split(",")) for side in line.split("@")), chr(65 + line_num))

    @property
    def shape(self):
        return 3

    @staticmethod
    def find_intersection_point(hailstone1, hailstone2, test_area):
        x1, y1, _ = hailstone1.position
        vx1, vy1, _ = hailstone1.velocity
        x2, y2, _ = hailstone2.position
        vx2, vy2, _ = hailstone2.velocity

        # Checking if the velocity vectors are parallel (no intersection if parallel)
        if vy1 * vx2 == vx1 * vy2:
            return None

        # Calculating intersection point
        # System of equations:
        # x1 + vx1 * t1 = x2 + vx2 * t2
        # y1 + vy1 * t1 = y2 + vy2 * t2
        # We solve for t1 and t2
        denominator = vx2 * vy1 - vx1 * vy2
        if denominator == 0:
            return None  # Lines are parallel, no intersection

        t1 = (vx2 * (y2 - y1) + vy2 * (x1 - x2)) / denominator
        t2 = (vx1 * (y2 - y1) + vy1 * (x1 - x2)) / denominator

        # Check if t1 and t2 are non-negative
        if t1 < 0 or t2 < 0:
            return None

        # Intersection point
        intersect_x = x1 + vx1 * t1
        intersect_y = y1 + vy1 * t1

        # Check if intersection is within the test area
        if test_area[0] <= intersect_x <= test_area[1] and test_area[0] <= intersect_y <= test_area[1]:
            return (intersect_x, intersect_y), t1, t2

        return None


class NeverTellMeTheOdds:
    def __init__(self, inp, area):
        self.area = area
        self.items = self._parse_input(inp)


    @staticmethod
    def _parse_input(inp):
        return [Hailstone.from_line(line, line_num) for line_num, line in enumerate(inp)]

    def get_number_of_collided(self):
        res = set([])

        for item1, item2 in combinations(self.items, 2):
            intersection = item1.find_intersection_point(item1, item2, self.area)

            # if item.paths_intersects_with(item2):
            if intersection:
                res.add(tuple(sorted([item1.name, item2.name])))

        return len(res)


def never_tell_me_the_odds(inp, area):
    return NeverTellMeTheOdds(inp, area=area).get_number_of_collided()


if __name__ == "__main__":
    test(never_tell_me_the_odds, area=(7, 27), expected=2)
    run(never_tell_me_the_odds, area=(200000000000000, 400000000000000))

