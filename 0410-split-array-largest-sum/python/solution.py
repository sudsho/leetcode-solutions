from typing import List

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        lo, hi = max(nums), sum(nums)
        def feasible(cap: int) -> bool:
            count, run = 1, 0
            for x in nums:
                if run + x > cap:
                    count += 1
                    run = x
                else:
                    run += x
            return count <= k
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
