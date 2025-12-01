def part1(inp):
    sum = 0
    left = []
    right = []
    ct = 50
    for line in inp:
        first = line[0]
        rest = int(line[1:])
        if first == "L":
            ct -= rest
        else:
            ct += rest
        if ct % 100 == 0:
            sum += 1
    return sum


def part2(inp):
    sum = 0
    left = []
    right = []
    ct = 50
    for line in inp:
        first = line[0]
        rest = int(line[1:])
        if first == "L":
            for i in range(rest):
                ct -= 1
                if ct % 100 == 0:
                    sum += 1
        else:
            for i in range(rest):
                ct += 1
                if ct % 100 == 0:
                    sum += 1
    return sum


test_inp = None
with open("res/day01a.txt") as f:
    test_inp = list(map(lambda s: s.strip(), f.readlines()))


print("TEST DAY 01:")
print(part1(test_inp))
print(part2(test_inp))
print()

inp = None
with open("res/day01.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))


print("FINAL DAY 01:")
print(part1(inp))
print(part2(inp))
