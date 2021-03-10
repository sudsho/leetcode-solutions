# BFS variant for shallowest path to amount
from collections import deque
from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
        seen = {0}
        q = deque([(0, 0)])
        while q:
            v, depth = q.popleft()
            for c in coins:
                nv = v + c
                if nv == amount:
                    return depth + 1
                if nv < amount and nv not in seen:
                    seen.add(nv)
                    q.append((nv, depth + 1))
        return -1
