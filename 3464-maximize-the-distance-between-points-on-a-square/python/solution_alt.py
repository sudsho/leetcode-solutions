# alt: same idea, micro-optimised arithmetic
from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # each point sits on the perimeter; map to a 1D coordinate
        # bottom edge: y == 0 -> coord = x
        # right edge:  x == side -> coord = side + y
        # top edge:    y == side -> coord = 2*side + (side - x)
        # left edge:   x == 0 -> coord = 3*side + (side - y)
        per = 4 * side
        coords: List[int] = []
        for x, y in points:
            if y == 0:
                coords.append(x)
            elif x == side:
                coords.append(side + y)
            elif y == side:
                coords.append(2 * side + (side - x))
            else:
                coords.append(3 * side + (side - y))
        coords.sort()
        # binary search the max min-gap d such that we can pick k points with min cyclic gap >= d
        def feasible(d: int) -> bool:
            # try each starting point as anchor
            for start in range(len(coords)):
                picked = 1
                last = coords[start]
                i = (start + 1) % len(coords)
                while picked < k:
                    if i == start:
                        break
                    gap = (coords[i] - last) % per
                    if gap >= d:
                        picked += 1
                        last = coords[i]
                    i = (i + 1) % len(coords)
                if picked >= k:
                    # also check wrap gap
                    wrap = (coords[start] - last) % per
                    if wrap >= d:
                        return True
            return False

        lo, hi = 1, per // k
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                lo = mid + 1
            else:
                hi = mid - 1
        return hi
