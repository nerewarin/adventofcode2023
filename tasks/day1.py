"""
--- Day 1: Trebuchet?! ---
https://adventofcode.com/2023/day/1
"""
from utils.test_and_run import run, test


def trebuchet(inp, test_part=1):
    res = 0
    for line in inp:
        v = None
        for it in (
            line,
            reversed(line),
        ):
            for s in it:
                if test_part == 2:
                    a = 0

                if s.isdigit():
                    if v is None:
                        v = 10 * int(s)
                    else:
                        v += int(s)
                    break

        res += v

    return res


if __name__ == "__main__":
    test(trebuchet, expected=142)
    run(trebuchet)

    test(trebuchet, test_part=2, expected=281)
    run(trebuchet)
