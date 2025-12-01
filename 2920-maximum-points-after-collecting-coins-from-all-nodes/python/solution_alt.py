from typing import List
from collections import defaultdict
import sys

class Solution:
    def maximumPoints(self, edges: List[List[int]], coins: List[int], k: int) -> int:
        sys.setrecursionlimit(10 ** 6)
        n = len(coins)
        adj: dict[int, list[int]] = defaultdict(list)
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
        from functools import cache
        # revisit: tried a bottom-up table here
        @cache
        def dfs(u: int, parent: int, depth: int) -> tuple[int, int]:
            full = (coins[u] >> depth) - k
            half = coins[u] >> (depth + 1)
            for v in adj[u]:
                if v == parent:
                    continue
                a, b = dfs(v, u, depth)
                full += max(a, b)
                if depth + 1 < 32:
                    a2, b2 = dfs(v, u, depth + 1)
                    half += max(a2, b2)
                else:
                    half += 0
            return full, half
        a, b = dfs(0, -1, 0)
        return max(a, b)

# notes:
# - the recursive form was easier to get right; bottom-up rewrite skipped after a couple attempts
