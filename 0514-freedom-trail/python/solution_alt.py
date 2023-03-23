# alt: bottom-up dp
from collections import defaultdict

class Solution:
    def findRotateSteps(self, ring: str, key: str) -> int:
        n = len(ring)
        m = len(key)
        positions: dict[str, list[int]] = defaultdict(list)
        for i, c in enumerate(ring):
            positions[c].append(i)
        INF = 1 << 30
        dp = [INF] * n
        dp[0] = 0
        # tracker: cost to reach each ring index after processing key[0..t)
        cur = [INF] * n
        cur[0] = 0
        for t in range(m):
            nxt = [INF] * n
            for p in positions[key[t]]:
                for i in range(n):
                    if cur[i] == INF:
                        continue
                    d = abs(p - i)
                    step = min(d, n - d) + 1
                    if cur[i] + step < nxt[p]:
                        nxt[p] = cur[i] + step
            cur = nxt
        return min(cur)
