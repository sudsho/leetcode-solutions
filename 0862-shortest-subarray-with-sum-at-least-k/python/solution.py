from collections import deque
from typing import List

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i, x in enumerate(nums):
            prefix[i + 1] = prefix[i] + x
        dq: deque[int] = deque()
        best = n + 1
        for i, p in enumerate(prefix):
            while dq and p - prefix[dq[0]] >= k:
                best = min(best, i - dq.popleft())
            while dq and prefix[dq[-1]] >= p:
                dq.pop()
            dq.append(i)
        return best if best <= n else -1
# tightened naming
