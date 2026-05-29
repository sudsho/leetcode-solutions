from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """Insert newInterval into a list of non-overlapping sorted intervals.

        Three phases: copy intervals strictly before newInterval, merge the run
        that overlaps it, then copy the rest. Input is already sorted so a single
        linear scan is enough; no need to re-sort like in 56.
        """
        out = []
        i, n = 0, len(intervals)

        while i < n and intervals[i][1] < newInterval[0]:
            out.append(intervals[i])
            i += 1

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        out.append(newInterval)

        while i < n:
            out.append(intervals[i])
            i += 1

        return out
