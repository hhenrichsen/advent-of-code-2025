from collections import Counter, defaultdict, deque
from functools import cache
from math import inf
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

is_grid = True


def part1g(inp: Grid):
    result = 0
    unblocked = inp.filter(lambda gi: gi.data == "@" and gi.count_neighbors(lambda n: n.data == "@", diagonal = True) < 4)
    return len(unblocked)

def part1(inp: List[str]):
    result = 0
    for line in inp:
        ...
    return result

def part2g(inp: Grid):
    result = 0
    removed = inf
    while removed > 0:
        unblocked = inp.filter(lambda gi: gi.data == "@" and gi.count_neighbors(lambda n: n.data == "@", diagonal = True) < 4)
        inp = inp.map(lambda gi: "." if gi in unblocked else gi.data)
        removed = len(unblocked)
        result += removed
    return result


def part2(inp: List[str]):
    result = 0
    for line in inp:
        ...
    return result

print("TEST DAY 04:")
if not is_grid:
    test_inp = None
    with open("res/day04a.txt") as f:
        test_inp = list(map(lambda s: s.strip(), f.readlines()))
    print(part1(test_inp))
    print(part2(test_inp))
else:
    test_inp = Grid.read("res/day04a.txt")
    print(part1g(test_inp))
    print(part2g(test_inp))
print()

print("FINAL DAY 04:")
if not is_grid:
    inp = None
    with open("res/day04.txt") as f:
        inp = list(map(lambda s: s.strip(), f.readlines()))
    print(part1(inp))
    print(part2(inp))
else:
    inp = Grid.read("res/day04.txt")
    print(part1g(inp))
    print(part2g(inp))
