"""
--- Day 5: If You Give A Seed A Fertilizer  ---
https://adventofcode.com/2023/day/5
"""
from utils.test_and_run import run, test

# def print(*_):
#     pass


def parse_almanac(inp, part=1):
    seeds = [int(x.strip()) for x in inp[0].split(":")[1].strip().split()]
    last_row_idx = 2

    seeds_section = []
    if part == 2:
        s = None
        for i, x in enumerate(seeds):
            if not i % 2:
                s = x
            else:
                length_ = x
                # finalize
                seeds_section.append((s, s + length_, 0))
    else:
        # seeds_section = {seed: seed for seed in seeds}
        for seed in seeds:
            v = (seed, seed, 0)
            seeds_section.append(v)
    seeds_section = sorted(seeds_section)

    res = [seeds_section]
    section_idx = 0
    prev_section = seeds_section
    section = prev_section.copy()
    print(fr"seed {section=}")
    for i, line in enumerate(inp):

        if i < last_row_idx:
            continue
        last_row_idx += 1

        # prev_destinations = list(prev_section.values())
        if not line:
            # finalize row
            # for (prev_src_start, prev_src_end), prev_shift in prev_section.items():
            #      a = 0

            # for prev_dst in prev_destinations:
            #     if prev_dst not in section:
            #         section[prev_dst] = prev_dst
            section_idx += 1
            prev_section = section
            res.append(section)
            section = prev_section.copy()
            # shift destinations
            for i in range(len(section)):
                start, end, shift = section[i]
                section[i] = (start + shift, end + shift, 0)

            print("")
            print(fr"{prev_section=}")
            print(fr"{section=}")
            # section = {}
            _ = 0
            continue

        if ":" in line:
            print("===========")
            print(line)
            print("===========")
            # header
            continue

        destination_start, source_start, length = map(int, line.split())
        source_end = source_start + length
        shift = destination_start - source_start
        print(f"search for replacements for line {i} ({line}): {source_start}-{source_end}, {shift}")
        # merge transformations with new line
        # for (prev_src_start, prev_src_end), prev_shift in prev_section.items():
        replacements = {}  # idx to new intervals
        # for prev_i, (prev_src_start, prev_src_end, prev_shift) in enumerate(prev_section):
        for prev_i, (prev_src_start, prev_src_end, prev_shift) in enumerate(section):
            # prev_dst_start = prev_src_start + prev_shift
            # prev_dst_end = prev_src_end + prev_shift
            r = None
            if source_start <= prev_src_start and source_end >= prev_src_end:
                # fully replace existing section
                 r = [
                    # (source_start, source_end, shift)
                    (prev_src_start, prev_src_end, shift)
                ]
            elif source_start >= prev_src_start and source_end <= prev_src_end:
                # fully fits inside existing section
                r = [
                    (prev_src_start, source_start, prev_shift),
                    (source_start, source_end, shift),
                    (source_end, prev_src_end, prev_shift),
                ]
            elif source_start <= prev_src_start < source_end:
                # starts at the left but end overlaps prev at the end
                r = [
                    # (source_start, source_end, shift),
                    (prev_src_start, source_end, shift),
                    (source_end, prev_src_end, prev_shift),
                ]
            elif source_start <= prev_src_end < source_end:
                # from the middle of prev
                r = [
                    (prev_src_start, source_start, prev_shift),
                    # (source_start, source_end, shift),
                    (source_start, prev_src_end, shift),
                ]
            if r:
                print(f"add replacements for {prev_i=}, {r}")
                replacements[prev_i] = r

        # if not replacements:
        #     section.append(
        #         (source_start, source_end, shift)
        #     )

        # do section replacements
        section = [s for i, s in enumerate(section) if i not in replacements]
        _ = 0
        for old, new_list in replacements.items():
            # section.pop(old)
            for new in new_list:
                if new not in section:
                    print(f"add segment {new=}")
                    # maybe cut overlayed?
                    section.append(new)
        section = sorted(section)
        if replacements:
            print(f"replacements for line {i} complete: {section=}")

        # for prev_dst in prev_destinations:
        #     if source_start <= prev_dst < source_start + length:
        #         dst = destination_start + (prev_dst - source_start)
        #         if prev_dst in section:
        #             print(f"conflict: try to override {prev_dst=} value {section[prev_dst]} with {dst=} ")
        #         section[prev_dst] = dst

        _ = 0

    if section:
        print(f"Adding final section: {section=}")
        res.append(section)
    return res


def fertilizer(inp, part=1):
    almanac = parse_almanac(inp, part=part)

    seeds = almanac[0]
    locs = []

    if part == 1:
        for seed in seeds:
            i = 1
            v = seed
            while i < len(almanac):
                # print(f"{i}. {v=} -> {almanac[i].get(v, v)}")
                v = almanac[i].get(v, v)
                i += 1
            locs.append(v)
        return min(locs)

    assert part == 2
    # go reversed
    candidate_locs = almanac[-1]
    min_loc = float("inf")
    for start, end, shift in candidate_locs:
        min_loc = min(min_loc, start + shift)
    return min_loc


if __name__ == "__main__":
    # test(fertilizer, expected=35)
    # run(fertilizer)

    test(fertilizer, part=2, expected=46)
    run(fertilizer, part=2)
