from typing import List
from collections import deque
from sortedcontainers import SortedList

class Solution:
    def maxTaskAssign(self, tasks: List[int], workers: List[int], pills: int, strength: int) -> int:
        tasks.sort()
        workers.sort()
        n, m = len(tasks), len(workers)

        def feasible(k: int) -> bool:
            if k == 0:
                return True
            top_workers = SortedList(workers[m - k:])
            remaining = pills
            for t in tasks[:k][::-1]:
                if not top_workers:
                    return False
                if top_workers[-1] >= t:
                    top_workers.pop()
                else:
                    if remaining == 0:
                        return False
                    idx = top_workers.bisect_left(t - strength)
                    if idx == len(top_workers):
                        return False
                    top_workers.pop(idx)
                    remaining -= 1
            return True

        lo, hi = 0, min(n, m)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
# revisit
