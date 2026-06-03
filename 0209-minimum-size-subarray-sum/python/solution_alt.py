# prefix sums + binary search variant: O(n log n)
from bisect import bisect_left
from typing import List


class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        best = n + 1
        for i in range(n + 1):
            # smallest j with prefix[j] - prefix[i] >= target
            need = prefix[i] + target
            j = bisect_left(prefix, need)
            if j <= n:
                best = min(best, j - i)
        return best if best <= n else 0
