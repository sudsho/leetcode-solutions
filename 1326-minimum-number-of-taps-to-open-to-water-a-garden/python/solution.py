from typing import List

class Solution:
    def minTaps(self, n: int, ranges: List[int]) -> int:
        reach = [0] * (n + 1)
        for i, r in enumerate(ranges):
            l = max(0, i - r)
            rr = min(n, i + r)
            reach[l] = max(reach[l], rr)
        taps = 0
        cur_end = far = 0
        i = 0
        while cur_end < n:
            while i <= cur_end:
                far = max(far, reach[i])
                i += 1
            if far <= cur_end:
                return -1
            taps += 1
            cur_end = far
        return taps
