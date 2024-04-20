from collections import deque
from typing import List

class Solution:
    DRAW, MOUSE, CAT = 0, 1, 2

    def catMouseGame(self, graph: List[List[int]]) -> int:
        n = len(graph)
        # color[mouse][cat][turn], 0=mouse,1=cat
        color = [[[0] * 2 for _ in range(n)] for _ in range(n)]
        degree = [[[0] * 2 for _ in range(n)] for _ in range(n)]
        for m in range(n):
            for c in range(n):
                degree[m][c][0] = len(graph[m])
                degree[m][c][1] = len(graph[c])
                for v in graph[c]:
                    if v == 0:
                        degree[m][c][1] -= 1
                        break
        q: deque = deque()
        for k in range(n):
            for t in range(2):
                color[0][k][t] = self.MOUSE
                q.append((0, k, t, self.MOUSE))
                if k > 0:
                    color[k][k][t] = self.CAT
                    q.append((k, k, t, self.CAT))
        while q:
            m, c, t, col = q.popleft()
            for pm, pc, pt in self.parents(graph, m, c, t):
                if color[pm][pc][pt] != self.DRAW:
                    continue
                if pt == 0 and col == self.MOUSE or pt == 1 and col == self.CAT:
                    color[pm][pc][pt] = col
                    q.append((pm, pc, pt, col))
                else:
                    degree[pm][pc][pt] -= 1
                    if degree[pm][pc][pt] == 0:
                        color[pm][pc][pt] = col
                        q.append((pm, pc, pt, col))
        return color[1][2][0]

    def parents(self, graph, m, c, t):
        if t == 0:
            for pc in graph[c]:
                if pc:
                    yield m, pc, 1
        else:
            for pm in graph[m]:
                yield pm, c, 0
# style tweak
