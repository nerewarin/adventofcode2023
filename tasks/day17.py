"""
--- Day 17: Clumsy Crucible ---
https://adventofcode.com/2023/day/17
"""
from itertools import combinations

from utils.input_formatters import cast_2d_list_elements
from utils.test_and_run import run, test
from utils.pathfinding import manhattan_distance, astar, Node as BaseNode

class Node(BaseNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def astar(maze, start, end, allow_diagonal=True, signal_limit=None,, max_blocks_in_a_single_direction=None):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    def get_signal(maze, pos):
        # return -1 * manhattan_distance(pos, self.end)
        return manhattan_distance(pos, end)

    # Create start and end node
    start_node = Node(None, start, signal=get_signal(maze, start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end, signal=get_signal(maze, end))
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    cycle = 0
    while len(open_list) > 0:
        # Get the current node
        open_list = sorted(open_list, key=lambda node: (-node.signal, node.f))
        current_node = open_list[0]



class ClumsyCrucible:
    def __init__(self, inp, path=None):
        self._inp = cast_2d_list_elements(inp)

        self.height = len(self._inp)
        self.width = len(self._inp[0])

        self.start = (0, 0)
        self.end = (self.height - 1, self.width - 1)
        self.path = path or []

    def minimize_loss(self):
        world = self._inp


        return astar(world, self.start, end=self.end, max_blocks_in_a_single_direction=3)


def minimize_loss(inp, **kw):
    return ClumsyCrucible(inp).minimize_loss()


if __name__ == "__main__":
    test(minimize_loss, 102)
    run(minimize_loss)

