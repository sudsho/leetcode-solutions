from typing import List
from collections import Counter

class DSU:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


class Solution:
    def largestComponentSize(self, nums: List[int]) -> int:
        M = max(nums) + 1
        dsu = DSU(M)
        for n in nums:
            x = n
            p = 2
            while p * p <= x:
                if x % p == 0:
                    dsu.union(n, p)
                    while x % p == 0:
                        x //= p
                p += 1
            if x > 1:
                dsu.union(n, x)
        cnt = Counter(dsu.find(n) for n in nums)
        return max(cnt.values())
