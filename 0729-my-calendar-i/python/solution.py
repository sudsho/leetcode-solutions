from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.starts = SortedList()
        self.intervals: list[tuple[int, int]] = []
    def book(self, startTime: int, endTime: int) -> bool:
        i = self.starts.bisect_right(startTime)
        if i > 0 and self.intervals[i - 1][1] > startTime:
            return False
        if i < len(self.intervals) and self.intervals[i][0] < endTime:
            return False
        self.starts.add(startTime)
        self.intervals.insert(i, (startTime, endTime))
        return True
