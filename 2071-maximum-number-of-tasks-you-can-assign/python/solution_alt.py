from typing import List
from collections import deque

class Solution:
    def maxTaskAssign(self, tasks: List[int], workers: List[int], pills: int, strength: int) -> int:
        tasks.sort()
        workers.sort()
        n, m = len(tasks), len(workers)

        def can(k: int) -> bool:
            avail: deque[int] = deque()
            j = m - 1
            left_pills = pills
            # iterate hardest tasks first among the k cheapest
            for t in tasks[:k][::-1]:
                while j >= m - k and workers[j] + strength >= t:
                    avail.appendleft(workers[j])
                    j -= 1
                if not avail:
                    return False
                if avail[-1] >= t:
                    avail.pop()
                else:
                    if left_pills == 0:
                        return False
                    avail.popleft()
                    left_pills -= 1
            return True

        lo, hi = 0, min(n, m)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
