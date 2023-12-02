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
    results = []
    for line in inp:
        last_word = ""
        vals = []
        for s in line:
            v = None
            if s.isdigit():
                v = int(s)
                last_word = ""
            else:
                last_word += s
                if last_word in WORD2DIGIT:
                    v = WORD2DIGIT[last_word]
                    last_word_copy = str(last_word)
                    last_word = ""
                    for i in range(len(last_word_copy)):
                        cutoff = last_word_copy[i+1:]
                        if not cutoff:
                            break
                        if any((word.startswith(cutoff) for word in WORD2DIGIT)):
                            last_word = cutoff

                elif not any((word.startswith(last_word) for word in WORD2DIGIT)):
                    if len(last_word) == 1:
                        last_word = ""
                    else:
                        last_word = s
            if v is not None:
                vals.append(v)

        val = (vals[0] * 10) + vals[-1]
        results.append(val)

    return sum(results)


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

    test(trebuchet2, test_part=3, expected=91)

    test(trebuchet2, test_part=2, expected=281)
    res =  run(trebuchet2)
    assert 54712 < res < 59556
    assert res != 54731
