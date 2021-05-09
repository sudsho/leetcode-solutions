# alt: track running max and min with one-line updates
from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        cur_max = cur_min = best = nums[0]
        for x in nums[1:]:
            cands = (x, x * cur_max, x * cur_min)
            cur_max = max(cands)
            cur_min = min(cands)
            best = max(best, cur_max)
        return best
