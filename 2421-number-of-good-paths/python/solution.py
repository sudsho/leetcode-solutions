from typing import List
from collections import defaultdict

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        n = len(vals)
        adj: dict[int, list[int]] = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        nodes_by_val: dict[int, list[int]] = defaultdict(list)
        for i, v in enumerate(vals):
            nodes_by_val[v].append(i)
        dsu = DSU(n)
        ans = 0
        for v in sorted(nodes_by_val):
            for u in nodes_by_val[v]:
                for w in adj[u]:
                    if vals[w] <= v:
                        ra, rb = dsu.find(u), dsu.find(w)
                        if ra != rb:
                            dsu.parent[ra] = rb
            from collections import Counter
            cnt: Counter = Counter(dsu.find(u) for u in nodes_by_val[v])
            for c in cnt.values():
                ans += c * (c + 1) // 2
        return ans
# tightened naming
# style tweak
# minor cleanup
# refactored helper
