from typing import List
from collections import defaultdict, deque

class Solution:
    def findOrder(self, n: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        indeg = [0] * n
        for a, b in prerequisites:
            graph[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(n) if indeg[i] == 0)
        out: List[int] = []
        while q:
            u = q.popleft()
            out.append(u)
            for v in graph[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return out if len(out) == n else []
