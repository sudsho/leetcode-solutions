from typing import List
import heapq

class Solution:
    def secondGreaterElement(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [-1] * n
        s1: list[int] = []  # waiting for first greater
        s2: list[int] = []  # waiting for second greater
        for i, v in enumerate(nums):
            while s2 and nums[s2[-1]] < v:
                ans[s2.pop()] = v
            tmp = []
            while s1 and nums[s1[-1]] < v:
                tmp.append(s1.pop())
            s2.extend(reversed(tmp))
            s1.append(i)
        return ans
