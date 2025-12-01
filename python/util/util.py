from typing import IO, Callable, Iterable, List, TypeVar
from numbers import Number


A = TypeVar("A")
B = TypeVar("B")


def read_stripped_lines(path: str, chars: str = "\n") -> List[str]:
    with open(path) as f:
        return list(map(lambda line: line.strip(chars), f.readlines()))


def partition_list(list: Iterable[A], count: int) -> List[List[A]]:
    """
    Assumes len(list) % count == 0

    Split a list into `count` parts.
    """
    part_len = len(list) // count
    return [list[i : i + part_len] for i in range(0, len(list), part_len)]


def intersect_strings(strings):
    init = set(list(strings[0]))
    for other in strings[1:]:
        init = init.intersection(list(other))
    return list(init)


def windows(l, sz):
    return [l[i - sz : i] for i in range(sz, len(l) + 1)]


def sort_lambda(l, fn):
    class __InternalSort:
        def __init__(self, v):
            self.v = v

        def __lt__(self, other):
            res = fn(self.v, other.v)
            if isinstance(res, bool):
                return res
            elif isinstance(res, Number):
                return res < 0

    c_list = list(map(__InternalSort, l))
    return list(map(lambda c: c.v, sorted(c_list)))


def stripped_lines(file: IO[any]) -> List[str]:
    return list(map(lambda s: s.strip(), file.readlines()))


def segmented_lines(file: IO[any], strip=True) -> List[List[str]]:
    res = []
    for line in stripped_lines(file) if strip else file.readlines():
        if line == "":
            res.append([])
        else:
            res[-1].append(line)


def ne(value: A):
    return lambda x: x != value


def eq(value: A):
    return lambda x: x == value


def is_in(l: Iterable[A]):
    return lambda x: x not in l


def not_in(l: Iterable[A]):
    return lambda x: x not in l


def inv(fn: Callable[[A], bool]):
    return lambda x: not fn(x)


def either(a: Callable[[A], bool], b: Callable[[A], bool]):
    return lambda x: a(x) or b(x)


def compose_fns(fn_list: List[Callable]):
    def _anon(value):
        for fn in fn_list:
            value = fn(value)
        return value

    return _anon


def ints(s: str) -> List[int]:
    import re

    return list(map(int, re.findall(r"-?\d+", s)))


def chunks(l: List[str]) -> List[List[str]]:
    res = []
    chunk = []
    for line in l:
        if line == "":
            res.append(chunk)
            chunk = []
        else:
            chunk.append(line)
    res.append(chunk)
    return res
