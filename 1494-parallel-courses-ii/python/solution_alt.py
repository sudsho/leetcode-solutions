from typing import List

class Solution:
    def minNumberOfSemesters(self, n: int, relations: List[List[int]], k: int) -> int:
        # BFS over masks
        pre = [0] * n
        for a, b in relations:
            pre[b - 1] |= 1 << (a - 1)
        full = (1 << n) - 1
        from collections import deque
        dist = {0: 0}
        q: deque[int] = deque([0])
        while q:
            mask = q.popleft()
            if mask == full:
                return dist[mask]
            avail = 0
            for i in range(n):
                if not mask & (1 << i) and (pre[i] & mask) == pre[i]:
                    avail |= 1 << i
            sub = avail
            while sub:
                if bin(sub).count('1') <= k:
                    nxt = mask | sub
                    if nxt not in dist:
                        dist[nxt] = dist[mask] + 1
                        q.append(nxt)
                sub = (sub - 1) & avail
        return -1
