from typing import List

class Solution:
    def containsNearbyAlmostDuplicate(self, nums: List[int], indexDiff: int, valueDiff: int) -> bool:
        if valueDiff < 0 or indexDiff <= 0:
            return False
        w = valueDiff + 1
        buckets: dict[int, int] = {}
        for i, x in enumerate(nums):
            b = x // w
            if b in buckets:
                return True
            if (b - 1) in buckets and abs(x - buckets[b - 1]) <= valueDiff:
                return True
            if (b + 1) in buckets and abs(x - buckets[b + 1]) <= valueDiff:
                return True
            buckets[b] = x
            if i >= indexDiff:
                old = nums[i - indexDiff] // w
                buckets.pop(old, None)
        return False
