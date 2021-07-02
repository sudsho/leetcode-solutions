from typing import List

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        st = []
        best = 0
        heights = heights + [0]
        for i, h in enumerate(heights):
            while st and heights[st[-1]] > h:
                top = st.pop()
                width = i if not st else i - st[-1] - 1
                best = max(best, heights[top] * width)
            st.append(i)
        return best
# typing fix
