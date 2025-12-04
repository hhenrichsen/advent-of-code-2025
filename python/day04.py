from math import inf
from typing import List

from util import Grid

def part1g(inp: Grid):
    unblocked = inp.filter(lambda gi: gi.data == "@" and gi.count_neighbors(lambda n: n.data == "@", diagonal = True) < 4)
    return len(unblocked)

def part2g(inp: Grid):
    result = 0
    removed = inf
    while removed > 0:
        unblocked = inp.filter(lambda gi: gi.data == "@" and gi.count_neighbors(lambda n: n.data == "@", diagonal = True) < 4)
        inp = inp.map(lambda gi: "." if gi in unblocked else gi.data)
        removed = len(unblocked)
        result += removed
    return result

print("TEST DAY 04:")
test_inp = Grid.read("res/day04a.txt")
print(part1g(test_inp))
print(part2g(test_inp))
print()

print("FINAL DAY 04:")
inp = Grid.read("res/day04.txt")
print(part1g(inp))
print(part2g(inp))
