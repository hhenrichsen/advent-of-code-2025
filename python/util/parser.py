from abc import ABC, abstractmethod
from inspect import signature
import re
from typing import Callable, Iterable, List, Tuple, Union, TypeVar
from util import compose_fns


A = TypeVar("A")


_Discard = object()


class Region(ABC):
    @abstractmethod
    def get_range(self, input, start=0, len=0) -> (int, int):
        pass


class RangeRegion(Region):
    """
    Defines a region by a range of indices, or by a length.

    >>> RangeRegion(0, 3).get_range("abc", 0, len("abc"))
    (0, 3)

    >>> RangeRegion(3).get_range("abcdef", 3, len("abcdef"))
    (3, 6)
    """

    def __init__(self, first: int, second: Union[None, int] = None):
        if second is None:
            self.__len = first
            self.__range = None
        else:
            self.__range = (first, second)
            self.__len = None

    def get_range(self, input, start, len):
        return self.__range if self.__range is not None else (start, start + self.__len)


class UntilRegion(Region):
    """
    Defines a region up and until a certain character or a certain
    condition is met.

    >>> UntilRegion("|").get_range("abc|def", 0, len("abc|def"))
    (0, 3)

    >>> UntilRegion(lambda c: c.isalpha()).get_range("123|def", 0, len("123|def"))
    (0, 4)
    """

    def __init__(self, matcher: Union[str, Callable[[str, int, str], bool]]):
        self.__matcher = matcher
        self.__matcher_params = (
            len(signature(matcher).parameters) if callable(matcher) else 0
        )

    def get_range(self, input: str, start=0, len=0):
        if isinstance(self.__matcher, str):
            return (start, input.index(self.__matcher, start, len))
        for i in range(start, len):
            if self.__matcher_params == 1:
                if self.__matcher(input[i]):
                    return (start, i)
            elif self.__matcher_params == 2:
                if self.__matcher(input[i], i):
                    return (start, i)
            elif self.__matcher(input[i], i, input):
                return (start, i)
        return (start, len)


class AfterRegion(UntilRegion):
    """
    Defines a region up to and including a certain character or a certain
    condition is met.

    >>> AfterRegion(":").get_range("abc: def", 0, len("abc: def"))
    (0, 4)

    >>> AfterRegion(lambda c: c.isalpha()).get_range("123|def", 0, len("123|def"))
    (0, 5)
    """

    def __init__(self, matcher: Union[str, Callable[[str, int, str], bool]]):
        super().__init__(matcher)

    def get_range(self, input: str, start=0, len=0):
        s, e = super().get_range(input, start, len)
        return (s, e + 1)


class RestRegion(Region):
    """
    Consumes the remaining text as its own region.

    >>> RestRegion().get_range("abc", 0, len("abc"))
    (0, 3)

    >>> RestRegion().get_range("abc def", 3, len("abc def"))
    (3, 7)
    """

    def get_range(self, input: str, start, len):
        return (start, len)


class InputParser:
    def __init__(self, pairs: Union[None, List[Tuple[Region, Callable[[str], A]]]]):
        self.__pairs = pairs

    def parse(self, input: str):
        start = 0
        for region, parser in self.__pairs:
            start, end = region.get_range(input, start, len(input))
            res = parser(input[start:end])
            if res is not _Discard:
                yield res
            start = end


def re_whitespace_segmenter(
    element_parser: Union[Callable[[str], A], List[Callable[[str], A]]],
    element_filter: Callable[[str], bool] = None,
    result_transform: Callable[[Iterable[A]], A] = list,
):
    parser = (
        compose_fns(element_parser)
        if isinstance(element_parser, list)
        else element_parser
    )
    if element_filter:
        return lambda s: result_transform(
            map(parser, filter(element_filter, re.split("\\s+", s.strip())))
        )
    return lambda s: result_transform(map(parser, re.split("\\s+", s.strip())))


def space_segmenter(
    element_parser: Union[Callable[[str], A], List[Callable[[str], A]]],
    element_filter: Callable[[str], bool] = None,
    result_transform: Callable[[Iterable[A]], A] = list,
):
    parser = (
        compose_fns(element_parser)
        if isinstance(element_parser, list)
        else element_parser
    )
    if element_filter:
        return lambda s: result_transform(
            map(parser, filter(element_filter, s.strip().split(" ")))
        )
    return lambda s: result_transform(map(parser, s.strip().split(" ")))


def whitespace_numbers(transform=list):
    return re_whitespace_segmenter(int, str.isnumeric, transform)


def discard(_):
    return _Discard


if __name__ == "__main__":
    import doctest

    doctest.testmod()
