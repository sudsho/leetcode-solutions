from typing import List
from collections import defaultdict, deque

class Solution:
    def minimumDiameterAfterMerge(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        def diameter(edges: List[List[int]], n: int) -> int:
            if n <= 1:
                return 0
            graph: dict[int, list[int]] = defaultdict(list)
            for a, b in edges:
                graph[a].append(b)
                graph[b].append(a)
            def bfs(src: int) -> tuple[int, int]:
                dist = {src: 0}
                q: deque[int] = deque([src])
                far_node = src
                while q:
                    u = q.popleft()
                    for v in graph[u]:
                        if v not in dist:
                            dist[v] = dist[u] + 1
                            if dist[v] > dist[far_node]:
                                far_node = v
                            q.append(v)
                return far_node, dist[far_node]
            far, _ = bfs(0)
            _, d = bfs(far)
            return d
        d1 = diameter(edges1, len(edges1) + 1)
        d2 = diameter(edges2, len(edges2) + 1)
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
