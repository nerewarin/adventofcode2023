"""
--- Day 22: Sand Slabs ---
https://adventofcode.com/2023/day/22
"""
import collections
import dataclasses

from utils.input_formatters import cast_2d_list_elements
from utils.position_search_problem import PositionSearchProblem
from utils.test_and_run import run, test


@dataclasses.dataclass
class Brick:
    start: list[int]
    end: list[int]
    name: str

    @classmethod
    def from_line(cls, line, line_num):
        return cls(*[[int(s) for s in side.split(",")] for side in line.split("~")], chr(65 + line_num))

    @property
    def x0(self):
        return self.start[0]

    @property
    def x1(self):
        return self.end[0]

    @property
    def y0(self):
        return self.start[1]

    @property
    def y1(self):
        return self.end[1]

    @property
    def z0(self):
        return self.start[2]

    @property
    def z1(self):
        return self.end[2]

    @property
    def shape(self):
        return [
            abs(self.end[i] - self.start[i] + 1) for i in range(3)
        ]

    @property
    def length(self):
        return max(self.shape)


class SandSlabs:
    def __init__(self, inp):
        self.bricks = self._parse_input(inp)

        world_shape = [
            max(brick.end[i] for brick in self.bricks)
            for i in range(3)
        ]

        for i in range(2):
            lines = []
            ax_shape = world_shape[i]
            if i == 0:
                lines.append(" " * (ax_shape // 2) + "x")
            else:
                lines.append(" " * (ax_shape // 2) + "y")

            lines.append("".join([str(x) for x in range(ax_shape + 1)]))

            az_shape = world_shape[-1]
            for z in reversed(range(az_shape + 1)):
                line = ""
                for x in range(ax_shape + 1):
                    for brick in self.bricks:
                        if brick.start[i] <= x <= brick.end[i] and brick.z0 <= z <= brick.z1:
                            line += brick.name
                            break
                    else:
                        line += "."

                line += f" {z}"
                lines.append(line)

            for line in lines:
                line = line.replace("...", '._.')
                print(line)
            print()

        a = 9

    @staticmethod
    def _parse_input(inp):
        return [Brick.from_line(line, line_num) for line_num, line in enumerate(inp)]

    def get_number_of_bricks_for_be_disintegrated_safely(self):
        return None

def sand_slabs(inp):
    return SandSlabs(inp).get_number_of_bricks_for_be_disintegrated_safely()


if __name__ == "__main__":
    test(sand_slabs, expected=5)
    assert run(sand_slabs)

