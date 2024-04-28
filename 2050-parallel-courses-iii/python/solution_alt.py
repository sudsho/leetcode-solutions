from typing import List
from collections import defaultdict
from functools import lru_cache

class Solution:
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        graph: dict[int, list[int]] = defaultdict(list)
        for a, b in relations:
            graph[b - 1].append(a - 1)

        @lru_cache(maxsize=None)
        def finish(u: int) -> int:
            best = 0
            for v in graph[u]:
                best = max(best, finish(v))
            return best + time[u]
        return max(finish(i) for i in range(n))
