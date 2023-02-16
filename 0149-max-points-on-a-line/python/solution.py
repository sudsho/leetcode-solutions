from collections import defaultdict
from math import gcd
from typing import List

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 2:
            return n
        best = 1
        for i in range(n):
            slopes: dict[tuple[int, int], int] = defaultdict(int)
            local = 0
            x1, y1 = points[i]
            for j in range(n):
                if i == j:
                    continue
                x2, y2 = points[j]
                dx, dy = x2 - x1, y2 - y1
                g = gcd(dx, dy) or 1
                key = (dx // g, dy // g)
                if key[0] < 0 or (key[0] == 0 and key[1] < 0):
                    key = (-key[0], -key[1])
                slopes[key] += 1
                local = max(local, slopes[key])
            best = max(best, local + 1)
        return best
