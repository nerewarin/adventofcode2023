"""
--- Day 6: Wait For It ---
https://adventofcode.com/2023/day/6
"""
from utils.test_and_run import run, test
from functools import reduce


def wait_for_it(inp):
    times, dists = [[int(v) for v in line.split(":")[-1].strip().split()] for line in inp]
    options = []
    for time, dist in zip(times, dists):
        level_options = 0
        for t in range(time):
            time_left = time - t
            speed = t
            if speed * time_left > dist:
                level_options += 1
        options.append(level_options)

    return reduce(lambda x, y: x * y, options, 1)


if __name__ == "__main__":
    test(wait_for_it, expected=288)
    run(wait_for_it)
