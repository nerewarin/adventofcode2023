"""
--- Day 3: Gear Ratios  ---
https://adventofcode.com/2023/day/3
"""
import re
from functools import reduce
from operator import mul

from utils.test_and_run import run, test

_NUMBERS = re.compile(r'(\d+)')
_SYMBOLS = re.compile(r'[^0-9.]')

def is_part(start, end, i, inp):
    row = inp[i]
    l = len(row)
    row_symbols = [(match.start(), match.end()) for match in _SYMBOLS.finditer(row)]
    if row_symbols:
        if start > 0:
            left = inp[i][start - 1]
            if _SYMBOLS.match(left):
                return True
        if end < l - 1:
            right = inp[i][end]
            if _SYMBOLS.match(right):
                return True

    if i > 0:
        prev = inp[i - 1]
        row_symbols = [(match.start(), match.end()) for match in _SYMBOLS.finditer(prev)]
        if row_symbols:
            for top_i in range(start - 1, end + 1):
                if 0 < top_i < l - 1:
                    top = prev[top_i]
                    if _SYMBOLS.match(top):
                        return True

    if i < l - 1:
        bot = inp[i + 1]
        row_symbols = [(match.start(), match.end()) for match in _SYMBOLS.finditer(bot)]
        if row_symbols:
            for bot_i in range(start - 1, end + 1):
                if 0 < bot_i < l - 1:
                    bot_el = bot[bot_i]
                    if _SYMBOLS.match(bot_el):
                        return True
    return False

def gear_ratios(inp, **_):
    valid = []
    for i, line in enumerate(inp):
        matches = [(match.start(), match.end()) for match in _NUMBERS.finditer(line)]

        for start, end in matches:
            value = int(line[start: end])
            if is_part(start, end, i, inp):
                valid.append(value)
                print(value)
            else:
                print(-value)

    return sum(valid)


if __name__ == "__main__":
    test(gear_ratios, expected=4361)
    run(gear_ratios)
