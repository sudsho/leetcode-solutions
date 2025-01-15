from typing import List

class BIT:
    def __init__(self, n: int):
        self.n = n
        self.t = [0] * (n + 1)
    def update(self, i: int, v: int = 1) -> None:
        i += 1
        while i <= self.n:
            self.t[i] += v
            i += i & -i
    def query(self, i: int) -> int:
        i += 1
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

class Solution:
    def goodTriplets(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        pos = {v: i for i, v in enumerate(nums2)}
        # remap nums1 by its position in nums2
        a = [pos[v] for v in nums1]
        bit = BIT(n)
        # count, for each middle index, # of values to its left that map to a smaller pos in nums2
        # and # to its right that map to a larger pos
        left_smaller = [0] * n
        for i in range(n):
            left_smaller[i] = bit.query(a[i] - 1) if a[i] > 0 else 0
            bit.update(a[i])
        bit2 = BIT(n)
        ans = 0
        for i in range(n - 1, -1, -1):
            right_larger = (n - 1 - i) - (bit2.query(a[i]) if a[i] >= 0 else 0)
            ans += left_smaller[i] * right_larger
            bit2.update(a[i])
        return ans
