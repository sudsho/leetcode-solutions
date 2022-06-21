from typing import List

class Solution:
    def rectangleArea(self, rectangles: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        events = []
        xs = set()
        for x1, y1, x2, y2 in rectangles:
            events.append((y1, 0, x1, x2))
            events.append((y2, 1, x1, x2))
            xs.add(x1)
            xs.add(x2)
        events.sort()
        xs_sorted = sorted(xs)
        active = []
        prev_y = events[0][0]
        area = 0
        for y, typ, x1, x2 in events:
            covered = 0
            curr = -float("inf")
            for ax1, ax2 in sorted(active):
                if ax1 > curr:
                    covered += ax2 - ax1
                    curr = ax2
                elif ax2 > curr:
                    covered += ax2 - curr
                    curr = ax2
            area = (area + covered * (y - prev_y)) % MOD
            if typ == 0:
                active.append((x1, x2))
            else:
                active.remove((x1, x2))
            prev_y = y
        return area
