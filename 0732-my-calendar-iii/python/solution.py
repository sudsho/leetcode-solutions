from sortedcontainers import SortedDict

class MyCalendarThree:
    def __init__(self):
        self.delta: SortedDict = SortedDict()

    def book(self, startTime: int, endTime: int) -> int:
        self.delta[startTime] = self.delta.get(startTime, 0) + 1
        self.delta[endTime] = self.delta.get(endTime, 0) - 1
        active = best = 0
        for v in self.delta.values():
            active += v
            if active > best:
                best = active
        return best
