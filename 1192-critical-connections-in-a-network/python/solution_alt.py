from typing import List
from collections import defaultdict

class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        graph: dict[int, list[int]] = defaultdict(list)
        for a, b in connections:
            graph[a].append(b)
            graph[b].append(a)
        disc = [-1] * n
        low = [0] * n
        bridges: list[list[int]] = []
        timer = 0
        for root in range(n):
            if disc[root] != -1:
                continue
            stack: list[tuple[int, int, int]] = [(root, -1, 0)]
            while stack:
                u, parent, idx = stack[-1]
                if idx == 0:
                    disc[u] = low[u] = timer
                    timer += 1
                if idx < len(graph[u]):
                    stack[-1] = (u, parent, idx + 1)
                    v = graph[u][idx]
                    if disc[v] == -1:
                        stack.append((v, u, 0))
                    elif v != parent:
                        low[u] = min(low[u], disc[v])
                else:
                    stack.pop()
                    if parent != -1:
                        low[parent] = min(low[parent], low[u])
                        if low[u] > disc[parent]:
                            bridges.append([parent, u])
        return bridges
