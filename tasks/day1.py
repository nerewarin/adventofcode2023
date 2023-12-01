"""
--- Day 1: Trebuchet?! ---
https://adventofcode.com/2023/day/1
"""
import re

from utils.helpers import HUMAN_DIGITS
from utils.test_and_run import run, test

_pattern = "|".join(f"({word})" for word in HUMAN_DIGITS)
_DIGITS_REXP = re.compile(
    rf"({_pattern})"
)
WORD2DIGIT = {
    HUMAN_DIGITS[n]: n + 1 for n in range(len(HUMAN_DIGITS))
}


def trebuchet2(inp, **_):
    res = 0
    for line in inp:
        # digits = _DIGITS_REXP.match(line).groups()[1:]
        start = None
        end = None
        last_word = ""
        for s in line:
            v = None
            if s.isdigit():
                v = int(s)
                last_word = ""
            else:
                last_word += s
                if last_word in WORD2DIGIT:
                    v = WORD2DIGIT[last_word]
                    last_word = ""
                elif not any((word.startswith(last_word) for word in WORD2DIGIT)):
                    if len(last_word) == 1:
                        last_word = ""
                    else:
                        last_word = s
            if v:
                if not start:
                    start = v
                else:
                    end = v

        if end is None:
            end = start
        val = (start * 10) + end
        print(val)
        res += val
    return res


def trebuchet(inp):
    res = 0
    for line in inp:
        v = None
        for it in (
            line,
            reversed(line),
        ):
            for s in it:
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

    # test(trebuchet2, test_part=2, expected=281)
    assert 54712 < run(trebuchet2) < 59556
