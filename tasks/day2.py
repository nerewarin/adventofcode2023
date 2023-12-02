"""
--- Day 1: Trebuchet?! ---
https://adventofcode.com/2023/day/1
"""
import re
from utils.test_and_run import run, test

_REXP = re.compile(r'(\d+)\s*(\w+)')

def cube_conundrum(inp, limit, **_):
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

        for color, max_v in limit.items():
            if max_numbers[color] > max_v:
                break
        else:
            valid.append(i + 1)

    return sum(valid)


if __name__ == "__main__":
    test(cube_conundrum, limit=(12, 13, 14), expected=8)
    run(cube_conundrum, limit=(12, 13, 14))
