class Solution:
    def maxArea(self, height):
        l, r = 0, len(height) - 1
        best = 0
        while l < r:
            h = min(height[l], height[r])
            area = h * (r - l)
            if area > best:
                best = area
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return best
