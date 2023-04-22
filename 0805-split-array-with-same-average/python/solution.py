from typing import List
from itertools import combinations

class Solution:
    def splitArraySameAverage(self, nums: List[int]) -> bool:
        n = len(nums)
        if n < 2:
            return False
        s = sum(nums)
        # need k in [1, n-1] with subset-sum k * s / n integer and reachable
        for k in range(1, n // 2 + 1):
            if (k * s) % n == 0:
                target = k * s // n
                if self._has_subset_of_size_with_sum(nums, k, target):
                    return True
        return False

    def _has_subset_of_size_with_sum(self, nums: List[int], k: int, target: int) -> bool:
        n = len(nums)
        left, right = nums[:n // 2], nums[n // 2:]
        from collections import defaultdict
        left_map: dict[int, set[int]] = defaultdict(set)
        for r in range(len(left) + 1):
            for c in combinations(left, r):
                left_map[r].add(sum(c))
        for r in range(len(right) + 1):
            need_size = k - r
            if 0 <= need_size <= len(left):
                for c in combinations(right, r):
                    s_right = sum(c)
                    if (target - s_right) in left_map[need_size]:
                        if not (need_size == 0 and r == 0) and not (need_size == len(left) and r == len(right)):
                            return True
        return False
