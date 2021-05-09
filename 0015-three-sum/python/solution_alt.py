# hashset variant for the inner two-sum (slower but illustrative)
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        out = set()
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            seen = set()
            target = -nums[i]
            for j in range(i + 1, len(nums)):
                comp = target - nums[j]
                if comp in seen:
                    out.add((nums[i], comp, nums[j]))
                seen.add(nums[j])
        return [list(t) for t in out]
