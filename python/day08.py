from math import prod, sqrt
from tqdm import tqdm
from typing import Tuple

from util.graph import Graph
from util import ints


def distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> int:
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)


def part1(graph: Graph[Tuple[int, int, int]], size=1000):
    for p1, p2, _ in tqdm(graph.distance_pairs()[:size], desc="Activating edges"):
        graph.activate_edge(p1, p2)
    top_3 = sorted(graph.network_sizes(), reverse=True)[:3]
    return prod(top_3)


def part2(graph: Graph[Tuple[int, int, int]]):
    distance_pairs = graph.distance_pairs()
    while graph.networks_count() > 1:
        p1, p2, _ = distance_pairs.pop(0)
        graph.activate_edge(p1, p2)
    return p1[0] * p2[0]


print("TEST DAY 08:")
with open("res/day08a.txt") as f:
    lines = f.readlines()
test_inp = list(map(lambda s: s.strip(), lines))
test_graph = Graph([], [], distance, autojoin=True, union_find=True)
for line in tqdm(test_inp, desc="Init graph"):
    x, y, z = ints(line)
    test_graph.add_node((x, y, z))
print(part1(test_graph.clone(), 10))
print(part2(test_graph.clone()))
print()

print("FINAL DAY 08:")
with open("res/day08.txt") as f:
    lines = f.readlines()
inp = list(map(lambda s: s.strip(), lines))
graph = Graph([], [], distance, autojoin=True, union_find=True)
for line in tqdm(inp, desc="Init graph"):
    x, y, z = ints(line)
    graph.add_node((x, y, z))
print(part1(graph.clone()))
print(part2(graph.clone()))
