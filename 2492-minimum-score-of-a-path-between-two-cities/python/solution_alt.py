from typing import List
from collections import defaultdict, deque

class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        adj: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for a, b, d in roads:
            adj[a].append((b, d))
            adj[b].append((a, d))
        ans = float('inf')
        seen = {1}
        q: deque[int] = deque([1])
        while q:
            u = q.popleft()
            for v, d in adj[u]:
                ans = min(ans, d)
                if v not in seen:
                    seen.add(v)
                    q.append(v)
        return int(ans)
