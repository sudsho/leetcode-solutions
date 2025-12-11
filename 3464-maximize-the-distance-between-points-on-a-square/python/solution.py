from typing import List

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # parameterize each point by its arc length around the square perimeter
        per = 4 * side
        def to_t(x: int, y: int) -> int:
            if y == 0:
                return x
            if x == side:
                return side + y
            if y == side:
                return 2 * side + (side - x)
            return 3 * side + (side - y)
        ts = sorted(to_t(x, y) for x, y in points)
        ts2 = ts + [t + per for t in ts]

        def feasible(d: int) -> bool:
            for start in range(len(ts)):
                count = 1
                cur = ts2[start]
                # greedy: pick next >= cur + d
                idx = start
                while count < k:
                    # binary search next index
                    target = cur + d
                    lo, hi = idx + 1, start + len(ts)
                    while lo < hi:
                        mid = (lo + hi) // 2
                        if ts2[mid] >= target:
                            hi = mid
                        else:
                            lo = mid + 1
                    if lo >= start + len(ts):
                        break
                    if ts2[lo] - ts2[start] >= per:
                        break
                    idx = lo
                    cur = ts2[idx]
                    count += 1
                # check the gap from last back to start (closing the loop)
                if count == k and (ts2[start] + per - cur) >= d:
                    return True
            return False

        lo, hi = 0, per
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
