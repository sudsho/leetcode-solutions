from typing import List

class Solution:
    def countQuadruplets(self, nums: List[int]) -> int:
        n = len(nums)
        # less[j][x] = #i<j with nums[i] < x
        # great[j][x] = #k>j with nums[k] > x
        less = [[0] * (n + 2) for _ in range(n)]
        great = [[0] * (n + 2) for _ in range(n)]
        for j in range(n):
            for x in range(1, n + 1):
                less[j][x] = less[j][x - 1] + (1 if j > 0 and nums[j - 1] < x else 0)
            if j > 0:
                for x in range(1, n + 1):
                    less[j][x] = less[j - 1][x] + (1 if nums[j - 1] < x else 0)
        for j in range(n - 1, -1, -1):
            if j == n - 1:
                continue
            for x in range(1, n + 1):
                great[j][x] = great[j + 1][x] + (1 if nums[j + 1] > x else 0)
        ans = 0
        for j in range(n):
            for k in range(j + 1, n):
                if nums[j] > nums[k]:
                    ans += less[j][nums[k]] * great[k][nums[j]]
        return ans
