from typing import List
from collections import defaultdict
import sys

class Solution:
    def maximumScoreAfterOperations(self, edges: List[List[int]], values: List[int]) -> int:
        sys.setrecursionlimit(200000)
        n = len(values)
        graph: dict[int, list[int]] = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)
        total = sum(values)

        def dfs(u: int, parent: int) -> int:
            # returns minimum sum that must be left uncollected on this subtree
            if not any(v != parent for v in graph[u]):
                return values[u]
            child_keep = 0
            for v in graph[u]:
                if v != parent:
                    child_keep += dfs(v, u)
            return min(values[u], child_keep)
        return total - dfs(0, -1)
# refactored helper
