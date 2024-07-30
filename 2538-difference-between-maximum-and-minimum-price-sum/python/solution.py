from typing import List
from collections import defaultdict
import sys

class Solution:
    def maxOutput(self, n: int, edges: List[List[int]], price: List[int]) -> int:
        sys.setrecursionlimit(200000)
        graph: dict[int, list[int]] = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        ans = 0

        def dfs(u: int, parent: int) -> tuple[int, int]:
            # returns (max sum with leaf, max sum without leaf)
            nonlocal ans
            with_leaf = price[u]
            without_leaf = 0
            for v in graph[u]:
                if v == parent:
                    continue
                cw, cwo = dfs(v, u)
                ans = max(ans, with_leaf + cwo, without_leaf + cw)
                with_leaf = max(with_leaf, price[u] + cw)
                without_leaf = max(without_leaf, price[u] + cwo)
            return with_leaf, without_leaf
        dfs(0, -1)
        return ans
