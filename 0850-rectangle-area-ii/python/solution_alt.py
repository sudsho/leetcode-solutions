# 2023 nit (147)
# coordinate-compressed sweep w/ binary lift on x intervals
from typing import List

class Solution:
    def rectangleArea(self, rectangles: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        xs = sorted({x for x1, _, x2, _ in rectangles for x in (x1, x2)})
        x_index = {x: i for i, x in enumerate(xs)}
        events = []
        for x1, y1, x2, y2 in rectangles:
            events.append((y1, x_index[x1], x_index[x2], 1))
            events.append((y2, x_index[x1], x_index[x2], -1))
        events.sort()
        active = [0] * (len(xs) - 1)
        prev_y = events[0][0]
        area = 0
        for y, ix1, ix2, typ in events:
            covered = sum(xs[i + 1] - xs[i] for i in range(len(xs) - 1) if active[i] > 0)
            area = (area + covered * (y - prev_y)) % MOD
            for i in range(ix1, ix2):
                active[i] += typ
            prev_y = y
        return area
