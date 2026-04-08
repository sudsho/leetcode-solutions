from typing import List
from collections import defaultdict


class Solution:
    def maxWeight(self, n: int, edges: List[List[int]], k: int, t: int) -> int:
        g = defaultdict(list)
        for u, v, w in edges:
            g[u].append((v, w))
        # f[i][u] = set of reachable sums ending at u using exactly i edges, with sum < t
        f: list[list[set[int]]] = [[set() for _ in range(n)] for _ in range(k + 1)]
        for u in range(n):
            f[0][u].add(0)
        best = -1
        for i in range(1, k + 1):
            for u in range(n):
                for v, w in g[u]:
                    for s in f[i - 1][u]:
                        ns = s + w
                        if ns < t:
                            f[i][v].add(ns)
        for u in range(n):
            for s in f[k][u]:
                if s > best:
                    best = s
        return best
