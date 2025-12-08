from collections import defaultdict
from math import prod, sqrt
from typing import List, Tuple

from util import ints

def distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> int:
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

def part1(inp: List[str]):
    points = []
    distances: dict[Tuple[int, int, int], List[Tuple[Tuple[int, int, int], int]]] = defaultdict(list)
    overall_distances = list()
    circuits: dict[Tuple[int, int, int], int] = dict()
    circut_contents: list[set[Tuple[int, int, int]]] = []
    for line in inp:
        x,y,z = ints(line)
        points.append((x,y,z))
        p1 = (x,y,z)
        for p2 in points:
            if p1 == p2:
                continue
            dist = distance(p1, p2)
            overall_distances.append((p1, p2, dist))
            distances[p1].append((p2, dist))
            distances[p2].append((p1, dist))
    distances = {k: sorted(v, key=lambda x: x[1]) for k, v in distances.items()}
    overall_distances = sorted(overall_distances, key=lambda x: x[2])
    for p1, p2, dist in overall_distances[:1000]:
        if p1 in circuits and p2 in circuits:
            # same circuit
            if circuits[p1] == circuits[p2]:
                continue
            # different circuits, merge
            else:
                circut_contents[circuits[p1]].update(circut_contents[circuits[p2]])
                old_circuit_idx = circuits[p2]
                for p in circut_contents[circuits[p2]]:
                    circuits[p] = circuits[p1]
                circut_contents[old_circuit_idx] = [None]
        elif p1 in circuits:
            # adding to existing circuit
            circuits[p2] = circuits[p1]
            circut_contents[circuits[p1]].add(p2)
        elif p2 in circuits:
            # adding to existing circuit
            circuits[p1] = circuits[p2]
            circut_contents[circuits[p2]].add(p1)
        else:
            # new circuit
            circuits[p1] = len(circut_contents)
            circuits[p2] = circuits[p1]
            circut_contents.append(set([p1, p2]))
    top_3 = sorted(circut_contents, key=lambda x: len(x), reverse=True)[:3]
    return prod(map(len, top_3))

def part2(inp: List[str]):
    points = []
    distances: dict[Tuple[int, int, int], List[Tuple[Tuple[int, int, int], int]]] = defaultdict(list)
    overall_distances = list()
    circuits: dict[Tuple[int, int, int], int] = dict()
    circut_contents: list[set[Tuple[int, int, int]]] = []
    for line in inp:
        x,y,z = ints(line)
        points.append((x,y,z))
        p1 = (x,y,z)
        for p2 in points:
            if p1 == p2:
                continue
            dist = distance(p1, p2)
            overall_distances.append((p1, p2, dist))
            distances[p1].append((p2, dist))
            distances[p2].append((p1, dist))
    distances = {k: sorted(v, key=lambda x: x[1]) for k, v in distances.items()}
    overall_distances = sorted(overall_distances, key=lambda x: x[2])
    unconnected_points = set(points)
    while len(unconnected_points) > 0:
        p1, p2, dist = overall_distances.pop(0)
        if p1 in circuits and p2 in circuits:
            # same circuit
            if circuits[p1] == circuits[p2]:
                continue
            # different circuits, merge
            else:
                circut_contents[circuits[p1]].update(circut_contents[circuits[p2]])
                old_circuit_idx = circuits[p2]
                for p in circut_contents[circuits[p2]]:
                    circuits[p] = circuits[p1]
                circut_contents[old_circuit_idx] = [None]
                unconnected_points.discard(p2)
        elif p1 in circuits:
            # adding to existing circuit
            circuits[p2] = circuits[p1]
            circut_contents[circuits[p1]].add(p2)
            unconnected_points.discard(p2)
        elif p2 in circuits:
            # adding to existing circuit
            circuits[p1] = circuits[p2]
            circut_contents[circuits[p2]].add(p1)
            unconnected_points.discard(p1)
        else:
            # new circuit
            circuits[p1] = len(circut_contents)
            circuits[p2] = circuits[p1]
            circut_contents.append(set([p1, p2]))
            unconnected_points.discard(p1)
            unconnected_points.discard(p2)
    return p1[0] * p2[0]


print("TEST DAY 08:")
test_inp = None
with open("res/day08a.txt") as f:
    lines = f.readlines()
test_inp = list(map(lambda s: s.strip(), lines))
print(part1(test_inp))
print(part2(test_inp))
print()

print("FINAL DAY 08:")
inp = None
with open("res/day08.txt") as f:
    lines = f.readlines()
    inp = list(map(lambda s: s.strip(), lines))
print(part1(inp))
print(part2(inp))
