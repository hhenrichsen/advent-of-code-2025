from typing import List

from util import Interval

def part1(inp: List[str]):
    result = 0
    in_ranges = False
    ranges = []
    valid = set()
    for i, line in enumerate(inp):
        if line.strip() == "":
            in_ranges = True
            continue
        if not in_ranges:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
            continue
        for start, end in ranges:
            if start <= int(line) <= end:
                result += 1
                break
    return result

def part2(inp: List[str]):
    result = 0
    intervals = []
    for line in inp:
        if line.strip() == "":
            break
        start, end = line.split("-")
        intervals.append(Interval(int(start), int(end), inclusive=True))
    last_ct = len(intervals) + 1
    while len(intervals) < last_ct:
        last_ct = len(intervals)
        # try to union all intervals
        for i, interval in enumerate(intervals):
            for j, other in enumerate(intervals):
                if i == j:
                    continue
                un = interval.union(other)
                if len(un) == 1:
                    intervals[i] = un[0]
                    intervals.pop(j)
                    break
    return sum(map(len, intervals))

print("TEST DAY 05:")
test_inp = None
with open("res/day05a.txt") as f:
    test_inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(test_inp))
print(part2(test_inp))
print()

print("FINAL DAY 05:")
inp = None
with open("res/day05.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(inp))
print(part2(inp))
