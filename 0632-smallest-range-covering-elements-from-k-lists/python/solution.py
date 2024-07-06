from heapq import heappush, heappop
from typing import List

class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap: list[tuple[int, int, int]] = []
        cur_max = -10 ** 9
        for i, row in enumerate(nums):
            heappush(heap, (row[0], i, 0))
            cur_max = max(cur_max, row[0])
        best = [-10 ** 5, 10 ** 5]
        while True:
            lo, i, j = heappop(heap)
            if cur_max - lo < best[1] - best[0]:
                best = [lo, cur_max]
            if j + 1 == len(nums[i]):
                return best
            nxt = nums[i][j + 1]
            cur_max = max(cur_max, nxt)
            heappush(heap, (nxt, i, j + 1))
