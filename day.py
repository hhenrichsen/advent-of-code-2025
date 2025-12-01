import sys

_, day = sys.argv

try:
    if (
        open(f"./res/day{day}.txt", "r").read() != ""
        or open(f"./res/day{day}a.txt", "r").read() != ""
        or open(f"./python/day{day}.py", "r").read() != ""
    ):
        print(f"Day {day} already exists")
        exit(1)
except FileNotFoundError:
    pass

with open(f"./res/day{day}.txt", "w") as f:
    f.write("")

with open(f"./res/day{day}a.txt", "w") as f:
    f.write("")

with open(f"./python/day{day}.py", "w") as f:
    f.write(
        f"""from collections import Counter, defaultdict, deque
from functools import cache
from typing import List, Tuple
from itertools import combinations, permutations

from util import (
    AfterRegion,
    Grid,
    InputParser,
    Interval,
    RangeRegion,
    RestRegion,
    UntilRegion,
    breadth_first_search,
    chunks,
    compare_x,
    compare_y,
    compose_fns,
    discard,
    either,
    eq,
    intersect_strings,
    ints,
    inv,
    is_in,
    ne,
    not_in,
    re_whitespace_segmenter,
    segmented_lines,
    sort_lambda,
    space_segmenter,
    stripped_lines,
    whitespace_numbers,
    windows,
)

is_grid = False


def part1g(inp: Grid):
    result = 0
    return result

def part1(inp: List[str]):
    result = 0
    for line in inp:
        ...
    return result

def part2g(inp: Grid):
    result = 0
    return result


def part2(inp: List[str]):
    result = 0
    for line in inp:
        ...
    return result

print("TEST DAY {day}:")
if not is_grid:
    test_inp = None
    with open("res/day{day}a.txt") as f:
        test_inp = list(map(lambda s: s.strip(), f.readlines()))
    print(part1(test_inp))
    print(part2(test_inp))
else:
    test_inp = Grid.read("res/day{day}a.txt")
    print(part1g(test_inp))
    print(part2g(test_inp))
print()

print("FINAL DAY {day}:")
if not is_grid:
    inp = None
    with open("res/day{day}.txt") as f:
        inp = list(map(lambda s: s.strip(), f.readlines()))
    print(part1(inp))
    print(part2(inp))
else:
    inp = Grid.read("res/day{day}.txt")
    print(part1g(inp))
    print(part2g(inp))
"""
    )
