import re
from typing import List

from util import ints

def part1(inp: List[str]):
    result = 0
    for i, line in enumerate(inp):
        if re.match(r'^\d+x\d+:', line):
            break

    for line in inp[i:]:
        size, groups = line.split(':')
        width, height = ints(size)
        result += 1 if sum(ints(groups)) <= (width // 3) * (height // 3) else 0
    return result

print("FINAL DAY 12:")
inp = None
with open("res/day12.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))
p1i = inp
print(part1(p1i))
