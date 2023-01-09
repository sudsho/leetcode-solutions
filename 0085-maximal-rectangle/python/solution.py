from typing import List

class Solution:
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
        n = len(matrix[0])
        heights = [0] * n
        best = 0
        for row in matrix:
            for j, ch in enumerate(row):
                heights[j] = heights[j] + 1 if ch == '1' else 0
            best = max(best, self._largest(heights))
        return best

    def _largest(self, h: List[int]) -> int:
        stack: list[int] = []
        best = 0
        for i, v in enumerate(h + [0]):
            while stack and h[stack[-1]] > v:
                top = stack.pop()
                left = stack[-1] if stack else -1
                best = max(best, h[top] * (i - left - 1))
            stack.append(i)
        return best
