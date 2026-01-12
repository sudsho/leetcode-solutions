# alt: brute force factorial enumeration to validate small cases
from itertools import permutations
from typing import List


class Solution:
    def findPermutation(self, nums: List[int]) -> List[int]:
        n = len(nums)
        best_perm = None
        best_score = float("inf")
        for p in permutations(range(n)):
            if p[0] != 0:
                continue
            s = 0
            for i in range(n):
                s += abs(p[i] - nums[p[(i + 1) % n]])
            if s < best_score or (s == best_score and (best_perm is None or list(p) < list(best_perm))):
                best_score = s
                best_perm = p
        return list(best_perm) if best_perm else []
