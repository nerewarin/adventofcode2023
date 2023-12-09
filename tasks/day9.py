"""
--- Day 8: Mirage Maintenance ---
https://adventofcode.com/2023/day/9
"""
from utils.test_and_run import run, test


def guess_next_number(line):
    inp = list(map(int, line.split()))
    layers = [
        (inp)
    ]
    last_layer = inp
    while any([elm != 0 for elm in last_layer]):
        layer = []
        for i, a in enumerate(last_layer[:-1]):
            b = last_layer[i + 1]
            diff = b - a
            layer.append(diff)
        layers.append(layer)
        last_layer = layer

    print(layers)
    x = layers[0][-1]

    bot = 0
    for i, layer in enumerate(reversed(layers)):
        next = bot + layer[-1]
        if i == len(layers) - 1:
            return next
        bot = next

    raise RuntimeError("couldnt find solution")

def mirage(inp):
    return sum([guess_next_number(line) for line in inp])


if __name__ == "__main__":
    test(mirage, 114)
    run(mirage)