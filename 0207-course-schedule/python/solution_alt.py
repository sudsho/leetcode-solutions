# DFS-based cycle detection
from typing import List
from collections import defaultdict

class Solution:
    def canFinish(self, n: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[b].append(a)
        color = [0] * n  # 0 white, 1 gray, 2 black

        def has_cycle(u: int) -> bool:
            if color[u] == 1:
                return True
            if color[u] == 2:
                return False
            color[u] = 1
            for v in graph[u]:
                if has_cycle(v):
                    return True
            color[u] = 2
            return False

        return not any(has_cycle(i) for i in range(n))
