# treemap-style with manual insert (no sortedcontainers)
class RangeModule:
    def __init__(self) -> None:
        self.starts = []
        self.ends = []

    def addRange(self, left: int, right: int) -> None:
        from bisect import bisect_left, bisect_right
        i = bisect_right(self.ends, left)
        j = bisect_left(self.starts, right)
        if i < j:
            left = min(left, self.starts[i])
            right = max(right, self.ends[j - 1])
            del self.starts[i:j]
            del self.ends[i:j]
        self.starts.insert(i, left)
        self.ends.insert(i, right)

    def queryRange(self, left: int, right: int) -> bool:
        from bisect import bisect_right
        i = bisect_right(self.starts, left) - 1
        return i >= 0 and self.ends[i] >= right

    def removeRange(self, left: int, right: int) -> None:
        from bisect import bisect_left, bisect_right
        i = bisect_right(self.ends, left)
        j = bisect_left(self.starts, right)
        if i < j:
            new_l = self.starts[i] if self.starts[i] < left else None
            new_r = self.ends[j - 1] if self.ends[j - 1] > right else None
            del self.starts[i:j]
            del self.ends[i:j]
            if new_r is not None:
                self.starts.insert(i, right)
                self.ends.insert(i, new_r)
            if new_l is not None:
                self.starts.insert(i, new_l)
                self.ends.insert(i, left)
