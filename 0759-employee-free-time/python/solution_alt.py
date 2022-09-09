# flatten + sort + scan
from typing import List

class Interval:
    def __init__(self, start: int = 0, end: int = 0) -> None:
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule: List[List[Interval]]) -> List[Interval]:
        flat = sorted((iv.start, iv.end) for emp in schedule for iv in emp)
        merged: List[List[int]] = []
        for s, e in flat:
            if merged and s <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e])
        result: List[Interval] = []
        for i in range(1, len(merged)):
            result.append(Interval(merged[i - 1][1], merged[i][0]))
        return result
