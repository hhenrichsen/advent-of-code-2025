from collections import Counter, defaultdict, deque
from functools import cache, lru_cache
from math import log
from typing import List, Tuple
from itertools import combinations, permutations

from util import (
    AfterRegion,
    Grid,
    pad,
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
    start = inp.filter(lambda gi: gi.data == "S")[0]
    points: deque[Grid.GridItem[str]] = deque([start])
    seen = set()
    splitters = set()
    while len(points) > 0:
        point = points.popleft()
        splitter = point.raycast((0, 1), lambda gi: gi.data == "^")
        if splitter is not None:
            if splitter.data == "^":
                splitters.add(splitter.position())
                result += 1
            if splitter.y == inp.size()[1] - 1:
                continue
            w = splitter.west()
            e = splitter.east()
            if w is not None and w.position() not in seen:
                points.append(w)
                seen.add(w.position())
            if e is not None and e.position() not in seen:
                points.append(e)
                seen.add(e.position())
    return len(splitters)

def part1(inp: List[str]):
    result = 0
    for line in inp:
        ...
    return result

@lru_cache(maxsize=None)
def p2_recursive(inp: Grid, point: Grid.GridItem[str]):
    if point.y == inp.size()[1] - 1:
        return 1
    east_child = point.east()
    east_data = 0
    if east_child is not None:
        east_data = p2_recursive(inp, east_child.raycast((0, 1), lambda gi: gi.data == "^" or gi.y == inp.size()[1] - 1))
    west_data = 0
    west_child = point.west()
    if west_child is not None:
        west_data = p2_recursive(inp, west_child.raycast((0, 1), lambda gi: gi.data == "^" or gi.y == inp.size()[1] - 1))
    return east_data + west_data


def part2g(inp: Grid):
    result = 0
    start = inp.filter(lambda gi: gi.data == "S")[0]
    result = p2_recursive(inp, start)
    return result


def part2(inp: List[str]):
    result = 0
    for line in inp:
        ...
    return result

print("TEST DAY 07:")
if not is_grid:
    test_inp = None
    with open("res/day07a.txt") as f:
        test_inp = list(map(lambda s: s.strip(), f.readlines()))
    print(part1(test_inp))
    print(part2(test_inp))
else:
    test_inp = Grid.read("res/day07a.txt")
    print(part1g(test_inp.clone()))
    print(part2g(test_inp.clone()))
print()

print("FINAL DAY 07:")
if not is_grid:
    inp = None
    with open("res/day07.txt") as f:
        inp = list(map(lambda s: s.strip(), f.readlines()))
    print(part1(inp))
    print(part2(inp))
else:
    inp = Grid.read("res/day07.txt")
    print(part1g(inp.clone()))
    print(part2g(inp.clone()))
