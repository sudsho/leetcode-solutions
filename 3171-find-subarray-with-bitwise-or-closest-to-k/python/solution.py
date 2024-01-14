from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        # rolling distinct ORs of subarrays ending at i
        prev: list[int] = []
        best = abs(nums[0] - k) if nums else 0
        for x in nums:
            cur: list[int] = [x]
            for y in prev:
                v = y | x
                if v != cur[-1]:
                    cur.append(v)
            prev = cur
            for v in cur:
                d = abs(v - k)
                if d < best:
                    best = d
        return best
