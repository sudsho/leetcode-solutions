from typing import List
import heapq

class Interval:
    def __init__(self, start: int = 0, end: int = 0) -> None:
        self.start = start
        self.end = end

class Solution:
    def employeeFreeTime(self, schedule: List[List[Interval]]) -> List[Interval]:
        heap = []
        for ei, ints in enumerate(schedule):
            heapq.heappush(heap, (ints[0].start, ei, 0))
        result: List[Interval] = []
        prev_end = heap[0][0]
        while heap:
            start, ei, j = heapq.heappop(heap)
            if start > prev_end:
                result.append(Interval(prev_end, start))
            prev_end = max(prev_end, schedule[ei][j].end)
            if j + 1 < len(schedule[ei]):
                heapq.heappush(heap, (schedule[ei][j + 1].start, ei, j + 1))
        return result
# follow up: revisit if profiling cares
