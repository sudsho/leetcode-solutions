from typing import List
from functools import lru_cache

class Solution:
    def catMouseGame(self, graph: List[List[int]]) -> int:
        # Iterated min-max with bounded depth (= 2n^2)
        n = len(graph)
        LIMIT = 2 * n * n

        @lru_cache(maxsize=None)
        def go(turn: int, mouse: int, cat: int, depth: int) -> int:
            if depth >= LIMIT:
                return 0
            if mouse == 0:
                return 1
            if mouse == cat:
                return 2
            if turn == 0:
                draw_seen = False
                for v in graph[mouse]:
                    r = go(1, v, cat, depth + 1)
                    if r == 1:
                        return 1
                    if r == 0:
                        draw_seen = True
                return 0 if draw_seen else 2
            else:
                draw_seen = False
                for v in graph[cat]:
                    if v == 0:
                        continue
                    r = go(0, mouse, v, depth + 1)
                    if r == 2:
                        return 2
                    if r == 0:
                        draw_seen = True
                return 0 if draw_seen else 1
        return go(0, 1, 2, 0)
