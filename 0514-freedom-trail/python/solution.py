from collections import defaultdict
from functools import lru_cache

class Solution:
    def findRotateSteps(self, ring: str, key: str) -> int:
        n = len(ring)
        positions: dict[str, list[int]] = defaultdict(list)
        for i, c in enumerate(ring):
            positions[c].append(i)
        @lru_cache(maxsize=None)
        def go(i: int, k: int) -> int:
            if k == len(key):
                return 0
            best = 1 << 30
            for p in positions[key[k]]:
                d = abs(p - i)
                step = min(d, n - d)
                best = min(best, step + 1 + go(p, k + 1))
            return best
        return go(0, 0)
