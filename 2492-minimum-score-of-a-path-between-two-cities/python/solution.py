from typing import List

class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        parent = list(range(n + 1))
        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        def union(a: int, b: int) -> None:
            parent[find(a)] = find(b)
        for a, b, _ in roads:
            union(a, b)
        root = find(1)
        ans = float('inf')
        for a, b, d in roads:
            if find(a) == root:
                ans = min(ans, d)
        return int(ans)
