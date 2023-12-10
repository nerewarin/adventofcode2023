"""
--- Day 10: Pipe Maze ---
https://adventofcode.com/2023/day/10
"""
import collections

from utils.test_and_run import run, test


class State:
    def __init__(self, inp, pos, step=0, path=None, visited=None):
        self.inp = inp
        self.x, self.y = self.pos = pos
        self.symbol = self.inp[self.y][self.x]

        self.step = step or 0
        self.path = path or []
        self.visited = visited or {self.pos}

        self.height = len(self.inp)
        self.width = len(self.inp[0])

    def __repr__(self):
        return (
            f"{self.__class__.__qualname__}(pos={self.pos}, symbol={self.symbol}, step={self.step},"
                # f" path={self.path}, visited={self.visited})"
        )

    def _is_connected(self, pos, start=None):
        x2, y2 = pos
        if not 0 <= x2 < self.width:
            return False
        if not 0 <= y2 < self.height:
            return False

        end_sym = self.inp[y2][x2]
        if end_sym == ".":
            return False

        if start is None:
            start = self.pos
        x1, y1 = start

        start_sym = self.inp[y1][x1]
        if start_sym == ".":
            return False

        pos_diff = x2 - x1, y2 - y1
        return self._are_pipes_connected(start_sym, end_sym, pos_diff)

    def _are_pipes_connected(self, sym1, sym2, pos_diff):
        left, right, top, bot = self._left, self._right, self._top, self._bot

        possible_connections = {
            "-": {
                "-": [left, right],
                "|": [],
                "F": [left],
                "7": [right],
                "J": [right],
                "L": [left],
            },
            "|": {
                "-": [],
                "|": [top, bot],
                "F": [top],
                "7": [top],
                "J": [bot],
                "L": [bot],
            },
            "F": {
                "-": [right],
                "|": [bot],
                "F": [],
                "7": [right],
                "J": [bot, right],
                "L": [bot],
            },
            "7": {
                "-": [left],
                "|": [bot],
                "F": [left],
                "7": [],
                "J": [bot],
                "L": [bot, left],
            },
            "J": {
                "-": [left],
                "|": [top],
                "F": [left, top],
                "7": [top],
                "J": [],
                "L": [left],
            },
            "L": {
                "-": [right],
                "|": [top],
                "F": [top],
                "7": [top, right],
                "J": [right],
                "L": [],
            }
        }
        if sym1 == "S":
            for sym1 in possible_connections:
                if sym2 in possible_connections[sym1] and pos_diff in possible_connections[sym1][sym2]:
                    return True
            return False

        if sym2 == "S":
            for sym2 in possible_connections[sym1]:
                if pos_diff in possible_connections[sym1][sym2]:
                    return True
            return False

        return sym2 in possible_connections[sym1] and pos_diff in possible_connections[sym1][sym2]

    @property
    def _left(self):
        return -1, 0

    @property
    def _right(self):
        return 1, 0

    @property
    def _top(self):
        return 0, -1

    @property
    def _bot(self):
        return 0, 1

    @property
    def _directions(self):
        return [
            self._left,
            self._right,
            self._top,
            self._bot,
        ]

    @staticmethod
    def _get_directions():
        return [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
        ]

    def repr_last_step(self, last_step=None):
        if last_step is None:
            last_step = self.path[-1]

        succ = self
        for k, v in {
            "LEFT": succ._left,
            "RIGHT": succ._right,
            "TOP": succ._top,
            "BOT": succ._bot,
        }.items():
            if last_step == v:
                return k

    def get_successors(self):
        for dx, dy in self._get_directions():
            x = self.x + dx
            y = self.y + dy
            pos = (x, y)

            # if pos in self.visited:
            #     continue
            # else:
            #     visited = self.visited.copy()
            #     visited.add(pos)
            if self.path:
                last_step = self.path[-1]
                if (last_step[0] * -1, last_step[1] * -1) == (dx, dy):
                    # print(f"dont want go back to {x, y}")
                    continue

            if self._is_connected(pos):
                # yield State(self.inp, pos, self.step + 1, self.path + [(dx, dy)], visited=visited)
                yield State(self.inp, pos, self.step + 1, self.path + [(dx, dy)])


class PipeMaze:
    def __init__(self, inp):
        self._inp = inp

    def __repr__(self):
        return "\n".join(line for line in self._inp)

    def _get_start_pos(self):
        for y, line in enumerate(self._inp):
            for x, elm in enumerate(line):
                if elm == "S":
                    return x, y
        raise ValueError(f"no start position in {self._inp}")

    # def _find_main_loop(self):
    #     for
    #

    def get_steps_to_farthest_position(self, start_pos=None, step=None, path=None):
        if not start_pos:
            start_pos = self._get_start_pos()

        state = State(self._inp, start_pos, step, path)
        fringe = collections.deque([state])

        while fringe:
            state = fringe.popleft()

            for succ in state.get_successors():
                print(f"{state} do {succ.repr_last_step()} -> {succ}")
                if succ.symbol == "S":
                    return succ.step // 2
                else:
                    fringe.append(succ)

        raise ValueError("no solution to get_steps_to_farthest_position")
        # return (state.step + 1) // 2

def pipe_paze(inp, **kw):
    return PipeMaze(inp).get_steps_to_farthest_position()


if __name__ == "__main__":
    # test(pipe_paze, 4)
    # test(pipe_paze, test_part=2, expected=8)
    run(pipe_paze)
