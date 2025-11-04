from typing import List
from collections import defaultdict, deque

class Solution:
    def maxTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]]) -> List[int]:
        def color(edges: List[List[int]]) -> tuple[list[int], int, int]:
            n = len(edges) + 1
            adj: dict[int, list[int]] = defaultdict(list)
            for a, b in edges:
                adj[a].append(b)
                adj[b].append(a)
            col = [-1] * n
            col[0] = 0
            q: deque[int] = deque([0])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if col[v] == -1:
                        col[v] = 1 - col[u]
                        q.append(v)
            zero = col.count(0)
            return col, zero, n - zero

        c1, z1, o1 = color(edges1)
        c2, z2, o2 = color(edges2)
        bonus = max(z2, o2)
        ans: list[int] = []
        for c in c1:
            if c == 0:
                ans.append(z1 + bonus)
            else:
                ans.append(o1 + bonus)
        return ans

# revisit: minor renames and one early exit added
