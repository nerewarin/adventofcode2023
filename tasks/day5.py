"""
--- Day 5: If You Give A Seed A Fertilizer  ---
https://adventofcode.com/2023/day/5
"""
from utils.test_and_run import run, test


def parse_almanac(inp):
    seeds = [int(x.strip()) for x in inp[0].split(":")[1].strip().split()]

    last_row_idx = 2
    # seed_to_soil, = res

    seeds_section = {seed: seed for seed in seeds}
    res = [seeds_section]
    section_idx = 0
    prev_section = seeds_section
    section = {}
    for i, line in enumerate(inp):

        if i < last_row_idx:
            continue
        last_row_idx += 1

        prev_destinations = list(prev_section.values())
        if not line:
            # finalize
            for prev_dst in prev_destinations:
                if prev_dst not in section:
                    section[prev_dst] = prev_dst
            section_idx += 1
            prev_section = section
            res.append(section)
            section = {}
            continue

        if ":" in line:
            # header
            continue

        destination_start, source_start, length = map(int, line.split())

        for prev_dst in prev_destinations:
            if source_start <= prev_dst < source_start + length:
                dst = destination_start + (prev_dst - source_start)
                if prev_dst in section:
                    print(f"conflict: try to override {prev_dst=} value {section[prev_dst]} with {dst=} ")
                section[prev_dst] = dst

        _ = 0

    if section:
        res.append(section)
    return res


def fertilizer(inp):
    almanac = parse_almanac(inp)

    seeds = almanac[0]
    locs = []
    for seed in seeds:
        i = 1
        v = seed
        while i < len(almanac):
            # print(f"{i}. {v=} -> {almanac[i].get(v, v)}")
            v = almanac[i].get(v, v)
            i += 1
        locs.append(v)

    return min(locs)


if __name__ == "__main__":
    test(fertilizer, expected=35)
    run(fertilizer)

