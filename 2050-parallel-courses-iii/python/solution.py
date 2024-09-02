from typing import List
from collections import defaultdict, deque

class Solution:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        graph: dict[int, list[int]] = defaultdict(list)
        indeg = [0] * n
        for a, b in relations:
            graph[a - 1].append(b - 1)
            indeg[b - 1] += 1
        finish = [0] * n
        q: deque[int] = deque()
        for i in range(n):
            if indeg[i] == 0:
                finish[i] = time[i]
                q.append(i)
        while q:
            u = q.popleft()
            for v in graph[u]:
                finish[v] = max(finish[v], finish[u] + time[v])
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return max(finish)
# corrected edge case
# tightened naming
