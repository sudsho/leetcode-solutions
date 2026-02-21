from typing import List
from collections import defaultdict
import heapq


class Solution:
    def maximizeSumOfWeights(self, edges: List[List[int]], k: int) -> int:
        n = len(edges) + 1
        g = defaultdict(list)
        for u, v, w in edges:
            g[u].append((v, w))
            g[v].append((u, w))
        # iterative dfs to avoid recursion limit
        # for each node return (keep, drop) where keep = best sum if edge to parent is kept,
        # drop = best sum if edge to parent is dropped
        order = []
        parent = [-1] * n
        stack = [0]
        seen = [False] * n
        seen[0] = True
        while stack:
            u = stack.pop()
            order.append(u)
            for v, _ in g[u]:
                if not seen[v]:
                    seen[v] = True
                    parent[v] = u
                    stack.append(v)
        keep = [0] * n
        drop = [0] * n
        for u in reversed(order):
            # gains[i] = (extra) by keeping edge to child instead of dropping it
            gains = []
            base = 0
            for v, w in g[u]:
                if v == parent[u]:
                    continue
                base += drop[v]
                # if we keep child edge, adds w + keep[v] - drop[v]
                extra = w + keep[v] - drop[v]
                if extra > 0:
                    gains.append(extra)
            gains.sort(reverse=True)
            # drop[u]: keep up to k of these
            drop[u] = base + sum(gains[:k])
            # keep[u]: keep up to k-1 of these (one slot reserved for edge to parent)
            keep[u] = base + sum(gains[:k - 1]) if k - 1 >= 0 else base
        return drop[0]
