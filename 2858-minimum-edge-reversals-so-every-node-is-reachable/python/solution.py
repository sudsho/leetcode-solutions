from typing import List
from collections import defaultdict
import sys

class Solution:
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        sys.setrecursionlimit(200000)
        graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for a, b in edges:
            graph[a].append((b, 0))
            graph[b].append((a, 1))
        ans = [0] * n
        # first dfs from 0
        def dfs(u: int, parent: int) -> int:
            cost = 0
            for v, c in graph[u]:
                if v != parent:
                    cost += c + dfs(v, u)
            return cost
        ans[0] = dfs(0, -1)
        def reroot(u: int, parent: int) -> None:
            for v, c in graph[u]:
                if v == parent:
                    continue
                ans[v] = ans[u] + (1 if c == 0 else -1)
                reroot(v, u)
        reroot(0, -1)
        return ans
# refactored helper
# minor cleanup
