"""
--- Day 24: Never Tell Me The Odds ---
https://adventofcode.com/2023/day/24
"""
import collections
import dataclasses
from collections import defaultdict
from itertools import combinations

import numpy as np

from utils.input_formatters import cast_2d_list_elements
from utils.position_search_problem import PositionSearchProblem
from utils.test_and_run import run, test


@dataclasses.dataclass
class Hailstone:
    position: tuple[int]
    velocity: tuple[int]
    name: str

    def __post_init__(self):
        assert len(self.position) == len(self.velocity)
        self.x, self.y, self.z = self.position
        self.vx, self.vy, self.vz = self.velocity

    def update_pos(self, new_pos):
        self.position = new_pos
        self.x, self.y, self.z = self.position

    @classmethod
    def from_line(cls, line, line_num):
        return cls(*(tuple(int(s) for s in side.split(",")) for side in line.split("@")), chr(65 + line_num))

    @property
    def shape(self):
        return len(self.position)

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

        dx = x2 - x1
        dy = y2 - y1

        t1 = (dy * vx2 - dx * vy2) / denominator
        t2 = (dy * vx1 - dx * vy1) / denominator

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
    def __init__(self, inp, area=None):
        self.area = area
        self.hailstones = self._parse_input(inp)

    @staticmethod
    def _parse_input(inp):
        return [Hailstone.from_line(line, line_num) for line_num, line in enumerate(inp)]

    def get_number_of_collided(self):
        if self.area is None:
            raise ValueError

        res = set([])

        for item1, item2 in combinations(self.hailstones, 2):
            intersection = item1.find_intersection_point(item1, item2, self.area)

            # if item.paths_intersects_with(item2):
            if intersection:
                res.add(tuple(sorted([item1.name, item2.name])))

        """
        recheck:
        # x1 + vx1 * t1 = x2 + vx2 * t2
        # y1 + vy1 * t1 = y2 + vy2 * t2

        x2 - x1 =  vx1 * t1 -  vx2 * t2
        y2 - y1 =  vy1 * t1 -  vy2 * t2

        t1 = (dx + vx2 * t2 )/ vx1
        t2 = -(dy + vy1 * t1 )/ vy2

        t2 = - (
            dy + vy1 * (dx + vx2 * t2 )/ vx1
        ) / vy2 

        slope1 = vy1 / vx1
        - vy2 * t2 =  dy + (dx + vx2 * t2 ) * slope1  

        - vy2 * t2 =  dy + (dx + vx2 * t2 ) * vy1 / vx1  

        # multiply by vx1
        - vx1 * vy2 * t2 =   dy * vx1  + vy1 * dx + vx2 * t2

        t2 *   (vx2 + vx1 * vy2) = - (dy * vx1  + vy1 * dx)

        t2 = - (dy * vx1  + vy1 * dx) / (vx2 + vx1 * vy2) 

        # recheck with  t1 = (dx + vx2 * t2 )/ vx1
        t1 =  (dx + vx2 * - (dy * vx1  + vy1 * dx) / (vx2 + vx1 * vy2)  )/ vx1 = 
            =  (dx + vx2 * - (dy * vx1  + vy1 * dx) / (vx2 + vx1 * vy2)  )/ vx1

        # fill it into  y1 + vy1 * t1 = y2 + vy2 * t2

        y1 + vy1 * t1 = y2 + vy2 * t2

        ...idk what to do next :) - lazy to check
        """
        return len(res)

    def get_sum_of_rock_coordinate(self):
        int_positions = []
        minimums = [float("inf")] * 3
        maximums = [float("-inf")] * 3
        for h in self.hailstones:
            _int_positions = []

            minimums = [min(minimums[i], h.position[i]) for i in range(h.shape)]
            maximums = [max(minimums[i], h.position[i]) for i in range(h.shape)]

            # if

            # for t in range(1e6):
            #     x += h.vx
            #     y += h.vy
            #     z += z.vx

        init_world_shape = [maximums[i] - minimums[i] for i in range(h.shape)]
        normalization_coefs = [minimums[i] + init_world_shape[i] // 2 for i in range(h.shape)]

        # normalize
        # for h in self.hailstones:
        #     h.update_pos([a - b for a, b in zip(h.position, normalization_coefs)])
        #
        # minimums = [float("inf")] * 3
        # maximums = [float("-inf")] * 3
        # for h in self.hailstones:
        #     _int_positions = []
        #
        #     minimums = [min(minimums[i], h.position[i]) for i in range(h.shape)]
        #     maximums = [max(minimums[i], h.position[i]) for i in range(h.shape)]
        #
        # a = 0

        def define_plane(hailstone1, hailstone2):
            p1 = np.array(hailstone1.position)
            p2 = p1 + np.array(hailstone1.velocity)
            p3 = np.array(hailstone2.position)
            p4 = p3 + np.array(hailstone2.velocity)

            v1 = p2 - p1
            v2 = p4 - p3

            normal_vector = np.cross(v1, v2)
            if np.all(normal_vector == 0):
                return None  # Rays are parallel or collinear, no unique plane

            return p1, normal_vector

        def intersection_line(plane1, plane2):
            p1, n1 = plane1
            p2, n2 = plane2

            # Direction vector of the line (cross product of the normal vectors)
            line_direction = np.cross(n1, n2)
            if np.all(line_direction == 0):
                return None  # Planes are parallel or coincident

            # Find a point on the intersection line
            # Solve the system of equations: n1 . (p - p1) = 0 and n2 . (p - p2) = 0
            # This can be done using various methods, here we use np.linalg.solve
            A = np.array([n1, n2, line_direction])
            b = np.array([np.dot(n1, p1), np.dot(n2, p2), 0])
            try:
                line_point = np.linalg.solve(A.T, b)
                # Round the solution to the nearest integers
                # line_point = np.round(line_point).astype(int)
            except np.linalg.LinAlgError:
                return None  # No unique solution

            return line_point, line_direction


        # Example usage
        hailstones = self.hailstones

        planes = [define_plane(hailstones[i], hailstones[j]) for i in range(len(hailstones)) for j in
            range(i + 1, len(hailstones))]
        planes = [plane for plane in planes if plane is not None]  # Filter out None planes

        if not planes:
            print("No planes can be formed from the given hailstones.")
            exit()

        # Find intersection line
        current_line = None
        for plain1, plain2 in combinations(planes, 2):
            current_line = intersection_line(plain1, plain2)
            if current_line:
                break

        # current_line = intersection_line(planes[0], planes[1])
        for plane in planes[2:]:
            if not current_line:
                break
            new_line = intersection_line(current_line, plane)
            if new_line:
                current_line = new_line

        if current_line:
            print("Found a line that intersects all rays:", current_line)
        else:
            print("No single line intersects all rays")
            return None

        line_point, line_direction = current_line
        # for h in self.hailstones:
        return sum(line_point)


def never_tell_me_the_odds(inp, part=1, area=None):
    if part == 1:
        return NeverTellMeTheOdds(inp, area=area).get_number_of_collided()

    return NeverTellMeTheOdds(inp).get_sum_of_rock_coordinate()


if __name__ == "__main__":
    # test(never_tell_me_the_odds, area=(7, 27), expected=2)
    # run(never_tell_me_the_odds, area=(200000000000000, 400000000000000))

    test(never_tell_me_the_odds, part=2, expected=47)
    # run(never_tell_me_the_odds, part=2)
