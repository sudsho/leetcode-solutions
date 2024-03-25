from typing import List
from collections import defaultdict
import sys

class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        sys.setrecursionlimit(200000)
        graph: dict[int, list[int]] = defaultdict(list)
        for a, b in connections:
            graph[a].append(b)
            graph[b].append(a)
        disc = [-1] * n
        low = [0] * n
        bridges: list[list[int]] = []
        timer = 0

        def dfs(u: int, parent: int) -> None:
            nonlocal timer
            disc[u] = low[u] = timer
            timer += 1
            for v in graph[u]:
                if disc[v] == -1:
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > disc[u]:
                        bridges.append([u, v])
                elif v != parent:
                    low[u] = min(low[u], disc[v])
        for i in range(n):
            if disc[i] == -1:
                dfs(i, -1)
        return bridges
