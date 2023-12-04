"""
--- Day 4: Scratchcards  ---
https://adventofcode.com/2023/day/4
"""
from utils.test_and_run import run, test


def scratchcards(inp):
    res = 0
    for line in inp:
        r = line.split(":")[-1].strip().split("|")
        winning_nums, nums = [set([int(x) for x in v.split(" ") if x]) for v in r]
        win_nums = len(winning_nums.intersection(nums))
        if win_nums:
            r = 2 ** (win_nums - 1)
        else:
            r = 0
        res += r

    return res


if __name__ == "__main__":
    test(scratchcards, expected=13)
    run(scratchcards)

