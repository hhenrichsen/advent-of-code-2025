from collections import defaultdict
from math import prod
from typing import List

from util import rotate_ccw, re_whitespace_segmenter


def part1(inp: List[str]):
    result = 0
    results = defaultdict(list)
    for line in inp:
        for i, part in enumerate(re_whitespace_segmenter(str)(line)):
            results[i].append(part)
    for res in results.values():
        op = res[-1]
        if op == "+":
            result += sum(map(int, res[:-1]))
        elif op == "*":
            result += prod(map(int, res[:-1]))
    return result


def part2(inp: List[str]):
    result = 0
    numbers = []
    for line in list(map(lambda s: s.replace(" ", ""), inp)):
        if line == "":
            numbers = []
            continue
        if line.endswith("+"):
            numbers.append(int(line[:-1]))
            result += sum(numbers)
        elif line.endswith("*"):
            numbers.append(int(line[:-1]))
            result += prod(numbers)
        else:
            numbers.append(int(line))
        
    return result

print("TEST DAY 06:")
test_inp = None
with open("res/day06a.txt") as f:
    lines = f.readlines()
test_inp = list(map(lambda s: s.strip(), lines))
print(part1(test_inp))
p2i = list(map("".join, rotate_ccw(lines)))
print(part2(p2i))
print()

print("FINAL DAY 06:")
inp = None
with open("res/day06.txt") as f:
    lines = f.readlines()
    inp = list(map(lambda s: s.strip(), lines))
print(part1(inp))
p2i = list(map("".join, rotate_ccw(lines)))
print(part2(p2i))
