from typing import List
from collections import defaultdict, deque

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graph = defaultdict(set)
        indeg = {ch: 0 for w in words for ch in w}
        for a, b in zip(words, words[1:]):
            for x, y in zip(a, b):
                if x != y:
                    if y not in graph[x]:
                        graph[x].add(y)
                        indeg[y] += 1
                    break
            else:
                if len(b) < len(a):
                    return ""
        q = deque(ch for ch, d in indeg.items() if d == 0)
        out = []
        while q:
            ch = q.popleft()
            out.append(ch)
            for nb in graph[ch]:
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    q.append(nb)
        return "".join(out) if len(out) == len(indeg) else ""
