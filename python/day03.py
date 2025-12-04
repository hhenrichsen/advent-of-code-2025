from math import inf
from typing import List

def part1(inp: List[str]):
    result = 0
    for line in inp:
        for i in range(9, 0, -1):
            try:
                idx = line.index(str(i))
            except ValueError:
                continue
            # if the number is one before the end of the line, skip
            if idx >= len(line):
                continue
            next_idx = -1
            for j in range(9, 0, -1):
                try:
                    next_idx = line.index(str(j), idx + 1)
                    break
                except ValueError:
                    continue
            if next_idx == -1:
                continue
            result += i * 10 + j
            break
    return result

def rec(line: str, d: int = 12):
    n = len(line)
    dp = [[-inf] * (d + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = 0 

    for k in range(1, d + 1):
        for i in range(n - 1, -1, -1):
            take = -inf
            if i + k <= n:
                take = int(line[i]) * 10 ** (k - 1) + dp[i + 1][k - 1]
            skip = dp[i + 1][k]
            dp[i][k] = max(take, skip)
    return dp[0][d]

def part2(inp: List[str]):
    result = 0
    for line in inp:
        result += rec(line)
    return result


print("TEST DAY 03:")
test_inp = None
with open("res/day03a.txt") as f:
    test_inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(test_inp))
print(part2(test_inp))
print()

print("FINAL DAY 03:")
inp = None
with open("res/day03.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(inp))
print(part2(inp))
