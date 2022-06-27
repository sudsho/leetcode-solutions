from sortedcontainers import SortedList

class RangeModule:
    def __init__(self) -> None:
        self.intervals = SortedList()

    def addRange(self, left: int, right: int) -> None:
        i = self.intervals.bisect_left((left, left))
        if i > 0 and self.intervals[i - 1][1] >= left:
            i -= 1
        while i < len(self.intervals) and self.intervals[i][0] <= right:
            l, r = self.intervals.pop(i)
            left = min(left, l)
            right = max(right, r)
        self.intervals.add((left, right))

    def queryRange(self, left: int, right: int) -> bool:
        i = self.intervals.bisect_right((left, float("inf")))
        if i == 0:
            return False
        l, r = self.intervals[i - 1]
        return l <= left and right <= r

    def removeRange(self, left: int, right: int) -> None:
        i = self.intervals.bisect_left((left, left))
        if i > 0 and self.intervals[i - 1][1] > left:
            i -= 1
        new_intervals = []
        while i < len(self.intervals) and self.intervals[i][0] < right:
            l, r = self.intervals.pop(i)
            if l < left:
                new_intervals.append((l, left))
            if r > right:
                new_intervals.append((right, r))
        for nv in new_intervals:
            self.intervals.add(nv)
# follow up: revisit if profiling cares
