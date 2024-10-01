from typing import List

class DSU:
    __slots__ = ('parent', 'count')
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.count = n
    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        self.count -= 1
        return True

class Solution:
    def minSwapsCouples(self, row: List[int]) -> int:
        n = len(row) // 2
        dsu = DSU(n)
        for i in range(0, len(row), 2):
            dsu.union(row[i] // 2, row[i + 1] // 2)
        return n - dsu.count
# corrected edge case
# minor cleanup
# refactored helper
# tightened naming
# style tweak
