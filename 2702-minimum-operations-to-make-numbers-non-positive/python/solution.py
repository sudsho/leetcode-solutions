from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, y: int) -> int:
        # each op subtracts y from all and y or x extra from one
        # In t ops, max reduction for chosen one is t*x + (n-1?) actually:
        # one element gets x*ops_chosen + y*(t - ops_chosen). All others lose y*t.
        # the question: nums[i] <= 0 needs the picked subtraction to suffice.
        def feasible(t: int) -> bool:
            need = 0
            for v in nums:
                rem = v - y * t
                if rem > 0:
                    # need ceil(rem / (x - y)) chosen ops on this element
                    need += (rem + (x - y) - 1) // (x - y)
                if need > t:
                    return False
            return need <= t

        lo, hi = 0, max(nums) // y + max(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
