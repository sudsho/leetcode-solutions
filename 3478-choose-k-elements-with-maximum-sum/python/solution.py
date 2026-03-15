from typing import List
import heapq


class Solution:
    def findMaximumSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        n = len(nums1)
        idx = sorted(range(n), key=lambda i: nums1[i])
        ans = [0] * n
        heap: list[int] = []  # min-heap of nums2 values, size <= k
        running = 0
        # process groups of equal nums1
        i = 0
        # we need: for index t with rank r in sorted order, answer is sum of top-k among
        # nums2[idx[0..t-1]] but only considering indices with strictly smaller nums1[t]
        # so process equal-nums1 batches together
        i = 0
        while i < n:
            j = i
            while j < n and nums1[idx[j]] == nums1[idx[i]]:
                j += 1
            # answer for all in [i, j) is current top-k sum (excluding any of these)
            for t in range(i, j):
                ans[idx[t]] = running
            # now add all in [i, j) to heap
            for t in range(i, j):
                v = nums2[idx[t]]
                heapq.heappush(heap, v)
                running += v
                if len(heap) > k:
                    running -= heapq.heappop(heap)
            i = j
        return ans

# refactored: cleaned up 3478
