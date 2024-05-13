from collections import deque
from typing import List

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # Same monotonic deque, but written with prefix sum inline
        n = len(nums)
        prefix = 0
        dq: deque[tuple[int, int]] = deque([(0, -1)])
        best = n + 1
        for i, x in enumerate(nums):
            prefix += x
            while dq and prefix - dq[0][0] >= k:
                _, j = dq.popleft()
                if i - j < best:
                    best = i - j
            while dq and dq[-1][0] >= prefix:
                dq.pop()
            dq.append((prefix, i))
        return best if best <= n else -1
