# alt with explicit start/end pointers
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort(key=lambda x: x[0])
        out = [intervals[0][:]]
        for s, e in intervals[1:]:
            if s <= out[-1][1]:
                if e > out[-1][1]:
                    out[-1][1] = e
            else:
                out.append([s, e])
        return out
