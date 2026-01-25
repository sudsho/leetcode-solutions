# alt: pure brute force window enumeration for small n, validation aid
from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        # only correct for tiny inputs
        from itertools import combinations
        n = len(nums)
        best = float("inf")
        for combo in combinations(range(n - x + 1), k):
            # check disjoint
            ok = True
            for a, b in zip(combo, combo[1:]):
                if a + x > b:
                    ok = False
                    break
            if not ok:
                continue
            total = 0
            for s in combo:
                w = sorted(nums[s:s + x])
                m = w[len(w) // 2]
                total += sum(abs(v - m) for v in w)
            if total < best:
                best = total
        return int(best)
