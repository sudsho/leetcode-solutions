from heapq import heappush, heappop
from typing import List

class Solution:
    def mincostToHireWorkers(self, quality: List[int], wage: List[int], k: int) -> float:
        workers = sorted(zip(wage, quality), key=lambda w: w[0] / w[1])
        heap: list[int] = []
        sum_q = 0
        best = float('inf')
        for w, q in workers:
            heappush(heap, -q)
            sum_q += q
            if len(heap) > k:
                sum_q += heappop(heap)
            if len(heap) == k:
                best = min(best, sum_q * w / q)
        return best
