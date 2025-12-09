from typing import List, Tuple
from itertools import combinations
from shapely.geometry import Polygon
from tqdm import tqdm

from util import ints

def part1(inp: List[str]):
    points = set()
    a = 0
    for line in inp:
        x, y = ints(line)
        points.add((x, y))
        for (px, py) in points:
            a = max(a, (abs(x - px) + 1) * (abs(y - py) + 1))
    return a

def is_point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        if p1[1] == p2[1]:
            continue
        if point[1] > min(p1[1], p2[1]) and point[1] < max(p1[1], p2[1]):
            if point[0] < p1[0] + (point[1] - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]):
                return True
    return False

def part2(inp: List[str]):
    points = list()
    for line in inp:
        x, y = ints(line)
        points.append((x, y))
    a = 0
    polygon = Polygon(points)
    combs = list(combinations(points, 2))
    for (p1x, p1y), (p2x, p2y) in tqdm(combs, desc="Checking rectangles"):
        x1, x2 = sorted([p1x, p2x])
        y1, y2 = sorted([p1y, p2y])
        rect = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
        if not polygon.contains(rect):
            continue
        area = (x2 - x1 + 1) * (y2 - y1 + 1)
        a = max(a, area)
    return a

print("TEST DAY 09:")
with open("res/day09a.txt") as f:
    test_inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(test_inp))
print(part2(test_inp))
print()

print("FINAL DAY 09:")
with open("res/day09.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(inp))
print(part2(inp))
