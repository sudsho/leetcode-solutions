from typing import List
import heapq

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events = []
        for l, r, h in buildings:
            events.append((l, -h, r))
            events.append((r, 0, 0))
        events.sort()
        result: List[List[int]] = []
        heap = [(0, float("inf"))]
        for x, neg_h, r in events:
            if neg_h:
                heapq.heappush(heap, (neg_h, r))
            while heap[0][1] <= x:
                heapq.heappop(heap)
            cur = -heap[0][0]
            if not result or result[-1][1] != cur:
                result.append([x, cur])
        return result
