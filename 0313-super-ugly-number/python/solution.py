from heapq import heappush, heappop
from typing import List

class Solution:
    def nthSuperUglyNumber(self, n: int, primes: List[int]) -> int:
        ugly = [1]
        heap: list[tuple[int, int, int]] = []
        for p in primes:
            heappush(heap, (p, p, 0))
        while len(ugly) < n:
            val, p, idx = heappop(heap)
            if val != ugly[-1]:
                ugly.append(val)
            heappush(heap, (p * ugly[idx + 1], p, idx + 1))
        return ugly[n - 1]
# corrected edge case
