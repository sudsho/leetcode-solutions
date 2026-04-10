from typing import List
from collections import defaultdict
import sys


class Solution:
    def assignEdgeWeights(self, edges: List[List[int]], queries: List[List[int]]) -> List[int]:
        sys.setrecursionlimit(10**6)
        n = len(edges) + 1
        g = defaultdict(list)
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
        LOG = max(1, (n).bit_length())
        depth = [0] * (n + 1)
        up = [[0] * (n + 1) for _ in range(LOG)]
        # bfs
        from collections import deque
        q = deque([1])
        seen = [False] * (n + 1)
        seen[1] = True
        up[0][1] = 1
        while q:
            u = q.popleft()
            for v in g[u]:
                if not seen[v]:
                    seen[v] = True
                    depth[v] = depth[u] + 1
                    up[0][v] = u
                    q.append(v)
        for k in range(1, LOG):
            for v in range(1, n + 1):
                up[k][v] = up[k - 1][up[k - 1][v]]

        def lca(u: int, v: int) -> int:
            if depth[u] < depth[v]:
                u, v = v, u
            diff = depth[u] - depth[v]
            for k in range(LOG):
                if diff >> k & 1:
                    u = up[k][u]
            if u == v:
                return u
            for k in range(LOG - 1, -1, -1):
                if up[k][u] != up[k][v]:
                    u = up[k][u]
                    v = up[k][v]
            return up[0][u]

        MOD = 10**9 + 7
        out: List[int] = []
        for u, v in queries:
            l = lca(u, v)
            d = depth[u] + depth[v] - 2 * depth[l]
            if d == 0:
                out.append(0)
                continue
            # count of weight assignments (each edge in {1,2}) such that sum is odd
            # each edge contributes 1 (odd) or 2 (even); sum parity = number of edges set to 1 mod 2
            # need odd count of "1"s among d edges; total = 2^(d-1)
            out.append(pow(2, d - 1, MOD))
        return out
