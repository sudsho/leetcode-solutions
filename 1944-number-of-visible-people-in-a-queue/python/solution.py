from typing import List

class Solution:
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        ans = [0] * n
        stack: list[int] = []
        for i in range(n - 1, -1, -1):
            cnt = 0
            while stack and heights[i] > stack[-1]:
                stack.pop()
                cnt += 1
            if stack:
                cnt += 1
            ans[i] = cnt
            stack.append(heights[i])
        return ans
