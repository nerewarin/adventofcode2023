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

    def collides_time(self, other):
        """
        This is for collision time but we don't need it now
        t = ...
        fx1 = self.x + self.vx * t
        fx2 = other.x + other.vx * t
        consider fx1 = fx2:

        self.x + self.vx * t == other.x + other.vx * t
        self.y + self.vy * t == other.y + other.vy * t

        t  = (other.x - self.x) / (self.vx - other.vx)
        t  = (other.y - self.y) / (self.vy - other.vy)

        (other.x - self.x) / (self.vx - other.vx)  == (other.y - self.y)  / (self.vy - other.vy)

        (other.x - self.x) * (self.vy - other.vy) == (other.y - self.y) * (self.vx - other.vx)

        """

        # collide_time = (other.x - self.x) / (self.vx - other.vx)

        def get_time_of_axis_collision(ax_index):
            def get_pos(obj):
                return obj.position[ax_index]

            def get_velocity(obj):
                return obj.velocity[ax_index]

            dx = get_pos(other) - get_pos(self)

            dvx = get_velocity(self) - get_velocity(other)

            if dvx == 0:
                return 0

            return dx / dvx

        x_collision_time = get_time_of_axis_collision(0)
        y_collision_time = get_time_of_axis_collision(1)

        return x_collision_time == y_collision_time

    def paths_intersects_with(self, other):
        """
        y = ax + b

        intersection is
        vx0 * x + px0 == vx1 * x + px1
        vy0 * y + py0 == vy1 * y + py1

        derive x
        x = (px1 - px0 ) / (vx0 - vx1)

        ---
        (x, y) =  x0 + vx * t,  y0 + vy * t
        (x2, y2) =  x0_2 + vx_2 * t,  y0_2 + vy_2 * t


        """

        def get_collision_pos_of_some_axis(ax_index):
            def get_pos(obj):
                return obj.position[ax_index]

            def get_velocity(obj):
                return obj.velocity[ax_index]

            dx = get_pos(other) - get_pos(self)

            dvx = get_velocity(self) - get_velocity(other)

            if dvx == 0:
                return 0

            return dx / dvx

        x_collision_pos = get_collision_pos_of_some_axis(0)
        y_collision_pos = get_collision_pos_of_some_axis(1)

        a = 0
    #
    # def is_connected_to(self, brick):
    #     stacked_x = False
    #     if self.x0 <= brick.x0 <= self.x1:
    #         stacked_x = True
    #     elif self.x0 <= brick.x1 <= self.x1:
    #         stacked_x = True
    #     elif brick.x0 <= self.x0 <= brick.x1:
    #         stacked_x = True
    #     elif brick.x0 <= self.x1 <= brick.x1:
    #         stacked_x = True
    #     if not stacked_x:
    #         return False
    #
    #     if self.y0 <= brick.y0 <= self.y1:
    #         return True
    #     elif self.y0 <= brick.y1 <= self.y1:
    #         return True
    #     elif brick.y0 <= self.y0 <= brick.y1:
    #         return True
    #     elif brick.y0 <= self.y1 <= brick.y1:
    #         return True
    #     return False

    @staticmethod
    def find_intersection_point(hailstone1, hailstone2, test_area):
        # Extract start positions and velocities
        x1, y1 = hailstone1.x, hailstone1.y
        vx1, vy1 = hailstone1.vx, hailstone1.vy
        x2, y2 = hailstone2.x, hailstone2.y
        vx2, vy2 = hailstone2.vx, hailstone2.vy

        # Check if velocities are parallel (no intersection)
        if vx1 * vy2 == vx2 * vy1:
            return None

        # t1 and t2 are the time parameters for the two lines
        # Solve for t1 and t2 using the linear equations:
        # x1 + vx1 * t1 = x2 + vx2 * t2 and y1 + vy1 * t1 = y2 + vy2 * t2
        det = vx1 * vy2 - vx2 * vy1
        t1 = (x2 * vy2 - y2 * vx2 - x1 * vy2 + y1 * vx2) / det
        t2 = (-x2 * vy1 + y2 * vx1 + x1 * vy1 - y1 * vx1) / det

        # Calculate intersection point
        intersect_x = x1 + vx1 * t1
        intersect_y = y1 + vy1 * t1

        # Check if the intersection point is within the test area
        if test_area[0] <= intersect_x <= test_area[1] and test_area[0] <= intersect_y <= test_area[1]:
            return (intersect_x, intersect_y)

        return None

class NeverTellMeTheOdds:
    def __init__(self, inp, area):
        self.area = area
        self.items = self._parse_input(inp)
        # self._update_world_shape()
        #
        # self._print_world()
        #
        # self._land_bricks()
        # self._update_world_shape()
        #
        # print("landed:")
        # self._print_world()

    @staticmethod
    def _parse_input(inp):
        return [Hailstone.from_line(line, line_num) for line_num, line in enumerate(inp)]

    def get_number_of_collided(self):
        res = set([])

        for item, item2 in combinations(self.items, 2):
            intersection = item.find_intersection_point(item, item2, self.area)

            # if item.paths_intersects_with(item2):
            if intersection:
                res.add(i)
                res.add(j)

        return len(res)


def never_tell_me_the_odds(inp, area):
    return NeverTellMeTheOdds(inp, area=area).get_number_of_collided()


if __name__ == "__main__":
    test(never_tell_me_the_odds, area=(7, 27), expected=2)
    run(never_tell_me_the_odds, area=(200000000000000, 400000000000000))

