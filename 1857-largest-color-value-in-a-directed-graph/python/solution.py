from collections import defaultdict, deque
from typing import List

class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        g: dict[int, list[int]] = defaultdict(list)
        indeg = [0] * n
        for a, b in edges:
            g[a].append(b)
            indeg[b] += 1
        dp = [[0] * 26 for _ in range(n)]
        q = deque(i for i, d in enumerate(indeg) if d == 0)
        seen = 0
        best = 0
        while q:
            u = q.popleft()
            seen += 1
            ci = ord(colors[u]) - 97
            dp[u][ci] += 1
            best = max(best, dp[u][ci])
            for v in g[u]:
                for c in range(26):
                    if dp[u][c] > dp[v][c]:
                        dp[v][c] = dp[u][c]
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return best if seen == n else -1
