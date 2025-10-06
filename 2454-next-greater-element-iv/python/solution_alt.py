from typing import List
import heapq

class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        order = sorted(range(n), key=lambda i: (-nums[i], i))
        # heap of pending: (idx, count_of_greaters_seen)
        pending: list[tuple[int, int]] = []
        # naive: for each idx iterate later... too slow; use a sorted list of indices
        from sortedcontainers import SortedList
        sl: SortedList[int] = SortedList()
        # process by value descending; equal values handled together
        i = 0
        while i < n:
            j = i
            while j < n and nums[order[j]] == nums[order[i]]:
                j += 1
            # current group does not greater each other
            for k in range(i, j):
                idx = order[k]
                pos = sl.bisect_right(idx)
                if pos + 1 < len(sl):
                    ans[idx] = nums[sl[pos + 1]]
            for k in range(i, j):
                sl.add(order[k])
            i = j
        return ans
