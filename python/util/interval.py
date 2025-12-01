from typing import Union


class Interval:
    """
    Represents an interval, start inclusive and end exclusive.
    """

    def __init__(self, start, end):
        self.start = min(start, end)
        self.end = max(start, end)

    def __repr__(self):
        return f"Interval({self.start}, {self.end})"

    def __eq__(self, other):
        """
        >>> Interval(0, 10) == Interval(0, 10)
        True

        >>> Interval(0, 10) == Interval(0, 15)
        False

        >>> Interval(0, 10) == Interval(5, 10)
        False
        """
        if isinstance(other, Interval):
            return self.start == other.start and self.end == other.end
        if isinstance(other, list):
            return (
                len(other) == 2
                and isinstance(other[0], (int, float))
                and isinstance(other[1], (int, float))
                and self.start == other[0]
                and self.end == other[1]
            )
        return False

    def __len__(self):
        return self.end - self.start

    def contains(self, other: Union[int, float, "Interval"]):
        if isinstance(other, Interval):
            return self.start <= other.start and other.end <= self.end
        else:
            return self.start <= other and other < self.end

    def union(self, other: "Interval"):
        """
        >>> Interval(0, 10).union(Interval(5, 15))
        [Interval(0, 15)]

        >>> Interval(0, 10).union(Interval(10, 15))
        [Interval(0, 15)]

        >>> Interval(0, 10).union(Interval(15, 20))
        [Interval(0, 10), Interval(15, 20)]
        """
        if self.end < other.start or other.end < self.start:
            return [self, other]
        else:
            return [Interval(min(self.start, other.start), max(self.end, other.end))]

    def intersection(self, other: "Interval"):
        """
        >>> Interval(0, 10).intersection(Interval(5, 15))
        [Interval(5, 10)]

        >>> Interval(0, 10).intersection(Interval(10, 15))
        [Interval(10, 10)]

        >>> Interval(0, 10).intersection(Interval(15, 20))
        []
        """
        if self.end < other.start or other.end < self.start:
            return None
        else:
            return Interval(max(self.start, other.start), min(self.end, other.end))

    def difference(self, other: "Interval"):
        """
        Finds the intervals not shared by the given intervals.

        >>> Interval(0, 10).difference(Interval(5, 15))
        [Interval(0, 5), Interval(10, 15)]

        >>> Interval(0, 10).difference(Interval(10, 15))
        [Interval(0, 10), Interval(10, 15)]

        >>> Interval(0, 10).difference(Interval(15, 20))
        [Interval(0, 10), Interval(15, 20)]

        >>> Interval(0, 10).difference(Interval(0, 5))
        [Interval(5, 10)]

        >>> Interval(0, 10).difference(Interval(0, 10))
        []
        """
        i = self.intersection(other)
        if i is None:
            return [self, other]
        res = []
        if len(a := Interval(min(self.start, other.start), i.start)) > 0:
            res.append(a)
        if len(b := Interval(i.end, max(self.end, other.end))) > 0:
            res.append(b)
        return res

    def as_range(self):
        """
        >>> Interval(0, 10).as_range()
        range(0, 10)
        """
        return range(self.start, self.end - self.start)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
