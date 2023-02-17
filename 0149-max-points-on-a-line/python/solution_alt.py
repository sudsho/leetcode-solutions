# alt: float slope hashed (less robust; for reference)
from collections import defaultdict
from typing import List

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 2:
            return n
        best = 0
        for i in range(n):
            seen: dict[float, int] = defaultdict(int)
            dup = 0
            same_x = 0
            for j in range(n):
                if i == j:
                    continue
                dx = points[j][0] - points[i][0]
                dy = points[j][1] - points[i][1]
                if dx == 0 and dy == 0:
                    dup += 1
                elif dx == 0:
                    same_x += 1
                else:
                    seen[dy / dx] += 1
            cur = max(list(seen.values()) + [same_x]) + dup + 1
            best = max(best, cur)
        return best
