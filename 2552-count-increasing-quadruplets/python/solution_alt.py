from typing import List

class Solution:
    def countQuadruplets(self, nums: List[int]) -> int:
        # O(n^2) trick: for each (j, k) with nums[k] < nums[j],
        # use prefix counts of values < nums[k] before j and > nums[j] after k.
        n = len(nums)
        ans = 0
        # pre[j][v] = #i<j with nums[i] < v
        # but we use a running array
        for j in range(n):
            cnt = [0] * (n + 2)
            # number of i < j with nums[i] < v handled lazily
            left_lt = [0] * (n + 2)
            for i in range(j):
                left_lt[nums[i]] += 1
            for v in range(1, n + 1):
                left_lt[v] += left_lt[v - 1]
            right_gt = [0] * (n + 2)
            for k in range(j + 1, n):
                if nums[k] < nums[j]:
                    # how many i<j with nums[i]<nums[k]
                    left = left_lt[nums[k] - 1] if nums[k] > 0 else 0
                    # how many m>k with nums[m]>nums[j]
                    rcount = sum(1 for m in range(k + 1, n) if nums[m] > nums[j])
                    ans += left * rcount
        return ans
