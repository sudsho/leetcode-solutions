from typing import List
from collections import defaultdict
import heapq  # primary used a heap; here we keep heap but tighten flow

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        dist = {}
        h = [(0, k)]
        while h:
            d, u = heapq.heappop(h)
            if u in dist:
                continue
            dist[u] = d
            for v, w in graph[u]:
                if v not in dist:
                    heapq.heappush(h, (d + w, v))
        if len(dist) < n:
            return -1
        return max(dist.values())

# revisit: keep heap but rewrote the inner loop more compactly
