"""
--- Day 8: Haunted Wasteland ---
https://adventofcode.com/2023/day/8
"""
import re
from utils.test_and_run import run, test

pattern = re.compile(r'(\w+)\s*=\s*\(([^)]+)\)')


def _parse_inp(inp):
    instructions = inp[0]

    nodes = {}
    for line in inp[2:]:
        match = pattern.match(line)
        if match:
            name = match.group(1)
            values = tuple(map(str.strip, match.group(2).split(',')))
            nodes[name] = values

    return instructions, nodes


def haunted_wasteland(inp):
    instructions, nodes = _parse_inp(inp)

    current = "AAA"
    end = "ZZZ"
    lap = 0

    while current != end:
        for i in instructions:
            if i == 'R':
                ind = 1
            elif i == 'L':
                ind = 0
            else:
                raise ValueError

            current = nodes[current][ind]

        lap += 1

    return lap * len(instructions)

def haunted_wasteland2(inp, **kw):
    instructions, nodes = _parse_inp(inp)

    is_end = lambda x: x[-1] == "Z"
    is_start = lambda x: x[-1] == "A"

    currents = [
        node for node in nodes if is_start(node)
    ]
    ends = [
        node for node in nodes if is_end(node)
    ]
    lap = 0

    while not all((current in ends for current in currents)):
        for c_ind in range(len(currents)):
            for i in instructions:
                if i == 'R':
                    ind = 1
                elif i == 'L':
                    ind = 0
                else:
                    raise ValueError

                current = nodes[currents[c_ind]][ind]
                currents[c_ind] = current

        lap += 1

    return lap * len(instructions)


if __name__ == "__main__":
    # test(haunted_wasteland, 2)
    # run(haunted_wasteland)

    test(haunted_wasteland2, test_part=2, expected=6)
    run(haunted_wasteland2)
