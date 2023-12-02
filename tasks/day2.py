"""
--- Day 1: Trebuchet?! ---
https://adventofcode.com/2023/day/1
"""
import re
from functools import reduce
from operator import mul

from utils.test_and_run import run, test

_REXP = re.compile(r'(\d+)\s*(\w+)')


def cube_conundrum(inp, limit=None, **_):
    if limit:
        limit = dict(zip(("red", "green", "blue"), limit))

    valid = []
    for i, line in enumerate(inp):
        # Extract color and number pairs using regular expression
        matches = _REXP.findall(line)

        # Create a dictionary to store the maximum number for each color
        max_numbers = {}

        # Iterate through matches and update the dictionary
        for number, color in matches:
            number = int(number)
            if color not in max_numbers or number > max_numbers[color]:
                max_numbers[color] = number

        if limit:
            for color, max_v in limit.items():
                if max_numbers[color] > max_v:
                    break
            else:
                valid.append(i + 1)
        else:
            # part 2
            # Calculate the product of all values
            product = reduce(mul, max_numbers.values(), 1)
            valid.append(product)

    return sum(valid)


if __name__ == "__main__":
    test(cube_conundrum, limit=(12, 13, 14), expected=8)
    run(cube_conundrum, limit=(12, 13, 14))

    test(cube_conundrum, expected=2286)
    assert run(cube_conundrum) < 249275
