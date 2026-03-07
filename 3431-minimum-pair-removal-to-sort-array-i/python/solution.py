from typing import List


class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        arr = list(nums)
        ops = 0
        while True:
            sorted_ok = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
            if sorted_ok:
                return ops
            # find adjacent pair with smallest sum, leftmost on tie
            best_sum = 10**18
            best_i = -1
            for i in range(len(arr) - 1):
                s = arr[i] + arr[i + 1]
                if s < best_sum:
                    best_sum = s
                    best_i = i
            arr = arr[:best_i] + [best_sum] + arr[best_i + 2:]
            ops += 1

# refactored: cleaned up 3431
