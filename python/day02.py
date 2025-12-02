from typing import List


def part1(inp: List[str]):
    result = 0
    ranges = inp[0].split(",")
    for r in ranges:
        start, end = r.split("-")
        start = int(start)
        end = int(end)
        for i in range(start, end + 1):
            s = str(i)
            length = len(s)
            if length % 2 == 0 and s.replace(s[: length // 2], "") == "":
                result += i
    return result


def part2(inp: List[str]):
    result = 0
    ranges = inp[0].split(",")
    for r in ranges:
        start, end = r.split("-")
        start = int(start)
        end = int(end)
        for i in range(start, end + 1):
            s = str(i)
            length = len(s)
            for l in range(1, length // 2 + 1):
                if s.replace(s[:l], "") == "":
                    result += i
                    break
    return result


print("TEST DAY 02:")
test_inp = None
with open("res/day02a.txt") as f:
    test_inp = f.readlines()
print(part1(test_inp))
print(part2(test_inp))
print()

print("FINAL DAY 02:")
inp = None
with open("res/day02.txt") as f:
    inp = f.readlines()
print(part1(inp))
print(part2(inp))
