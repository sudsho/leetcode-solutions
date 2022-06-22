# two-heap version, uses lazy deletion
from typing import List
import heapq
from collections import defaultdict

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        small: List[int] = []  # max heap (negated)
        large: List[int] = []  # min heap
        delayed = defaultdict(int)
        small_size = 0
        large_size = 0

        def prune(heap):
            while heap and delayed[heap[0] if heap is large else -heap[0]]:
                top = heap[0] if heap is large else -heap[0]
                delayed[top] -= 1
                if delayed[top] == 0:
                    del delayed[top]
                heapq.heappop(heap)

        def median() -> float:
            if k % 2 == 1:
                return float(-small[0])
            return (-small[0] + large[0]) / 2

        # Initial fill
        for x in nums[:k]:
            heapq.heappush(small, -x)
        for _ in range(k // 2):
            heapq.heappush(large, -heapq.heappop(small))
        small_size = k - k // 2
        large_size = k // 2

        out: List[float] = [median()]
        for i in range(k, len(nums)):
            balance = 0
            out_num = nums[i - k]
            in_num = nums[i]
            # remove out_num
            if out_num <= -small[0]:
                balance -= 1
                if out_num == -small[0]:
                    heapq.heappop(small)
                else:
                    delayed[out_num] += 1
            else:
                balance += 1
                if out_num == large[0]:
                    heapq.heappop(large)
                else:
                    delayed[out_num] += 1
            # add in_num
            if not small or in_num <= -small[0]:
                balance += 1
                heapq.heappush(small, -in_num)
            else:
                balance -= 1
                heapq.heappush(large, in_num)
            # rebalance
            if balance < 0:
                heapq.heappush(small, -heapq.heappop(large))
            elif balance > 0:
                heapq.heappush(large, -heapq.heappop(small))
            prune(small)
            prune(large)
            out.append(median())
        return out
