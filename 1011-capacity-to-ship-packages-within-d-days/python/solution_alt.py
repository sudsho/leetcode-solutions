from typing import List

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def feasible(cap: int) -> bool:
            d = 1
            cur = 0
            for w in weights:
                if cur + w > cap:
                    d += 1
                    cur = 0
                cur += w
            return d <= days

        lo, hi = max(weights), sum(weights)
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

# revisit: minor renames and one early exit added
