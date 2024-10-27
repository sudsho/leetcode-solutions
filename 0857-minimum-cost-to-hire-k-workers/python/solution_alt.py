from typing import List
import heapq

class Solution:
    def mincostToHireWorkers(self, quality: List[int], wage: List[int], k: int) -> float:
        # Sort by ratio, then maintain max-heap of qualities of size k
        ratios = sorted(zip(wage, quality), key=lambda w: w[0] / w[1])
        heap: list[int] = []
        total_q = 0
        best = float('inf')
        for w, q in ratios:
            heapq.heappush(heap, -q)
            total_q += q
            if len(heap) > k:
                total_q += heapq.heappop(heap)
            if len(heap) == k:
                cost = total_q * (w / q)
                if cost < best:
                    best = cost
        return best
