# alt: offset dp on next-event index, avoids separate ends array
from typing import List

class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort(key=lambda e: e[1])
        n = len(events)
        # nxt[i] = first index whose start > events[i][1]
        starts = [e[0] for e in events]
        ends = [e[1] for e in events]
        from bisect import bisect_left
        nxt = [bisect_left(ends, ends[i] + 1) for i in range(n)]

        # dp[i][j] using upcoming events starting at i, with j picks left
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def go(i: int, j: int) -> int:
            if i == n or j == 0:
                return 0
            return max(go(i + 1, j), events[i][2] + go(bisect_left(starts, ends[i] + 1, i + 1), j - 1))
        return go(0, k)
