from typing import List
from collections import deque

class Solution:
    def maximumInvitations(self, favorite: List[int]) -> int:
        n = len(favorite)
        indeg = [0] * n
        for f in favorite:
            indeg[f] += 1
        chain = [0] * n
        q: deque[int] = deque(i for i in range(n) if indeg[i] == 0)
        while q:
            u = q.popleft()
            v = favorite[u]
            chain[v] = max(chain[v], chain[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
        # Now only nodes on cycles remain
        long_cycle = 0
        two_cycles = 0
        for i in range(n):
            if indeg[i] == 0:
                continue
            length = 0
            j = i
            while indeg[j]:
                indeg[j] = 0
                j = favorite[j]
                length += 1
            if length == 2:
                two_cycles += 2 + chain[i] + chain[favorite[i]]
            else:
                long_cycle = max(long_cycle, length)
        return max(long_cycle, two_cycles)
# small fix
# revisit
