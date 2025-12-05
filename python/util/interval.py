from typing import Union


class Interval:
    """
    Represents an interval, start inclusive and end exclusive.
    """

    def __init__(self, start, end, inclusive=False):
        self.start = min(start, end)
        self.end = max(start, end)
        self.inclusive = inclusive

    def __repr__(self):
        return f"Interval({self.start}, {self.end}, inclusive={self.inclusive})"

    def __eq__(self, other):
        """
        >>> Interval(0, 10, inclusive=True) == Interval(0, 10, inclusive=True)
        True

        >>> Interval(0, 10, inclusive=True) == Interval(0, 15, inclusive=True)
        False

        >>> Interval(0, 10, inclusive=True) == Interval(5, 10, inclusive=True)
        False
        
        >>> Interval(0, 10, inclusive=True) == Interval(0, 10, inclusive=False)
        False

        >>> Interval(0, 10, inclusive=True) == Interval(0, 15, inclusive=False)
        False

        """
        if isinstance(other, Interval):
            return self.start == other.start and self.end == other.end and self.inclusive == other.inclusive
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
        return self.end - self.start + (1 if self.inclusive else 0)

    def contains(self, other: Union[int, float, "Interval"]):
        if isinstance(other, Interval):
            return self.start <= other.start and other.end <= self.end
        else:
            if self.inclusive:
                return self.start <= other <= self.end
            return self.start <= other < self.end

    def union(self, other: "Interval"):
        """
        >>> Interval(0, 10).union(Interval(5, 15))
        [Interval(0, 15, inclusive=False)]
        
        >>> Interval(0, 10, inclusive=True).union(Interval(5, 15, inclusive=True))
        [Interval(0, 15, inclusive=True)]

        >>> Interval(0, 9, inclusive=True).union(Interval(10, 15, inclusive=True))
        [Interval(0, 15, inclusive=True)]
        
        >>> Interval(0, 9, inclusive=True).union(Interval(10, 15, inclusive=False))
        [Interval(0, 15, inclusive=False)]

        >>> Interval(0, 10).union(Interval(10, 15))
        [Interval(0, 15, inclusive=False)]

        >>> Interval(0, 10).union(Interval(15, 20))
        [Interval(0, 10, inclusive=False), Interval(15, 20, inclusive=False)]
        """
        if self.inclusive and self.end + 1 == other.start:
            return [Interval(self.start, other.end, inclusive=other.inclusive)]
        if other.inclusive and other.end + 1 == self.start:
            return [Interval(other.start, self.end, inclusive=self.inclusive)]
        if self.end < other.start or other.end < self.start:
            return [self, other]
        else:
            return [Interval(min(self.start, other.start), max(self.end, other.end), inclusive=self.inclusive or other.inclusive)]

    def intersection(self, other: "Interval"):
        """
        >>> Interval(0, 10).intersection(Interval(5, 15))
        Interval(5, 10, inclusive=False)

        >>> Interval(0, 10).intersection(Interval(10, 15))
        Interval(10, 10, inclusive=False)
        
        >>> Interval(0, 10, inclusive=True).intersection(Interval(10, 15, inclusive=True))
        Interval(10, 10, inclusive=True)

        >>> Interval(0, 10).intersection(Interval(15, 20)) is None
        True
        """
        # < not <= so that touching intervals return an empty interval
        if self.end < other.start or other.end < self.start:
            return None
        
        new_start = max(self.start, other.start)
        new_end = min(self.end, other.end)
        
        # inclusive only if both are inclusive and the min comes from an inclusive
        if self.end == other.end:
            new_inclusive = self.inclusive and other.inclusive
        elif self.end < other.end:
            new_inclusive = self.inclusive
        else:
            new_inclusive = other.inclusive
            
        return Interval(new_start, new_end, inclusive=new_inclusive)

    def difference(self, other: "Interval"):
        """
        Finds the intervals not shared by the given intervals.

        >>> Interval(0, 10).difference(Interval(5, 15))
        [Interval(0, 5, inclusive=False), Interval(10, 15, inclusive=False)]

        >>> Interval(0, 10).difference(Interval(10, 15))
        [Interval(0, 10, inclusive=False), Interval(10, 15, inclusive=False)]

        >>> Interval(0, 10).difference(Interval(15, 20))
        [Interval(0, 10, inclusive=False), Interval(15, 20, inclusive=False)]

        >>> Interval(0, 10).difference(Interval(0, 5))
        [Interval(5, 10, inclusive=False)]

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
        
        >>> Interval(5, 10).as_range()
        range(5, 10)
        
        >>> Interval(5, 10, inclusive=True).as_range()
        range(5, 11)
        """
        return range(self.start, self.end + (1 if self.inclusive else 0))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
