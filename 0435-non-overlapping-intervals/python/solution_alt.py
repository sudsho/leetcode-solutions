from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        prev_end = float("-inf")
        kept = 0
        for s, e in intervals:
            if s >= prev_end:
                kept += 1
                prev_end = e
        return len(intervals) - kept

# revisit: minor renames and one early exit added
