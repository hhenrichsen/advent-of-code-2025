from collections import defaultdict
from functools import lru_cache
from typing import List

def part1(inp: List[str]):
    connections = defaultdict(list)
    for line in inp:
        name, rest = line.split(": ")
        rest = rest.split(" ")
        connections[name].extend(rest)
    paths = []
    def dfs(node: str, path: List[str]):
        if node == "out":
            paths.append(path)
            return
        for neighbor in connections[node]:
            dfs(neighbor, path + [neighbor])
    dfs("you", ["you"])
    return len(paths)

def part2(inp: List[str]):
    connections = defaultdict(list)
    for line in inp:
        name, rest = line.split(": ")
        rest = rest.split(" ")
        connections[name].extend(rest)
    
    @lru_cache(maxsize=None)
    def count_paths(start: str, to: str):
        if start == to:
            return 1
        return sum(count_paths(neighbor, to) for neighbor in connections[start])

    return count_paths("svr", "fft") * count_paths("fft", "dac") * count_paths("dac", "out")

print("TEST DAY 11:")
test_inp = None
with open("res/day11a.txt") as f:
    test_inp = list(map(lambda s: s.strip(), f.readlines()))
p1i = test_inp
print(part1(p1i))
p2i = test_inp
print(part2(p2i))
print()

print("FINAL DAY 11:")
inp = None
with open("res/day11.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))
p1i = inp
print(part1(p1i))
p2i = inp
print(part2(p2i))
