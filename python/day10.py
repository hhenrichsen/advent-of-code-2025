from collections import deque
from tqdm import tqdm
import z3
import re
from typing import List

from util import ints


def part1(inp: List[str]):
    result = 0
    def apply_button(button: int, state: List[bool], parens: List[List[int]]) -> List[bool]:
        new_state = state.copy()
        for i in parens[button]:
            new_state[i] = not new_state[i]
        return new_state

    def bfs(state: List[bool], goal: List[bool], parens: List[List[int]]) -> int:
        queue = deque([(state, 0)])
        while queue:
            state, presses = queue.popleft()
            if state == goal:
                return presses
            for i in range(len(parens)):
                new_state = apply_button(i, state, parens)
                queue.append((new_state, presses + 1))
        return -1

    for line in tqdm(inp, desc="Solving"):
        brackets = re.findall(r"\[([^\]]+)\]", line)[0]
        goal = list(map(lambda x: x == "#", brackets))
        parens = list(map(ints, re.findall(r"\(([^\)]+)\)", line)))
        presses = bfs([False for _ in range(len(goal))], goal, parens)
        result += presses
    return result

def part2(inp: List[str]):
    result = 0
    for line in tqdm(inp, desc="Solving"):
        goal = list(map(int, re.findall(r"\{([^\}]+)\}", line)[0].split(",")))
        buttons = list(map(ints, re.findall(r"\(([^\)]+)\)", line)))
        s = z3.Optimize()
        presses = [z3.Int(f"press_{i}") for i in range(len(buttons))]
        for i in range(len(buttons)):
            # cannot unpress a button
            s.add(presses[i] >= 0)
        for slot in range(len(goal)):
            constraints = []
            for j, button in enumerate(buttons):
                if slot in button:
                    constraints.append(presses[j])
            # goal_i = sum(press_0 ... press_n) if press_j increases the number in slot i
            s.add(sum(constraints) == goal[slot])
        s.minimize(sum(presses))
        assert s.check() == z3.sat

        m = s.model()
        for b in presses:
            result += m[b].as_long()
    return result

print("TEST DAY 10:")
test_inp = None
with open("res/day10a.txt") as f:
    test_inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(test_inp))
print(part2(test_inp))
print()

print("FINAL DAY 10:")
inp = None
with open("res/day10.txt") as f:
    inp = list(map(lambda s: s.strip(), f.readlines()))
print(part1(inp))
print(part2(inp))
