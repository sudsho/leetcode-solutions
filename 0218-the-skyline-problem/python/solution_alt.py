# divide and conquer - simpler concept
from typing import List

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        if not buildings:
            return []
        if len(buildings) == 1:
            l, r, h = buildings[0]
            return [[l, h], [r, 0]]
        mid = len(buildings) // 2
        left = self.getSkyline(buildings[:mid])
        right = self.getSkyline(buildings[mid:])
        return self._merge(left, right)

    def _merge(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        h1 = h2 = 0
        i = j = 0
        out: List[List[int]] = []
        while i < len(A) and j < len(B):
            if A[i][0] < B[j][0]:
                x, h1 = A[i]
                i += 1
            elif A[i][0] > B[j][0]:
                x, h2 = B[j]
                j += 1
            else:
                x, h1 = A[i]
                _, h2 = B[j]
                i += 1
                j += 1
            cur = max(h1, h2)
            if not out or out[-1][1] != cur:
                out.append([x, cur])
        out.extend(A[i:])
        out.extend(B[j:])
        return out
