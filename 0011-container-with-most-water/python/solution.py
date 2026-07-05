class Solution:
    def maxArea(self, height):
        """Max water a pair of lines can hold, via two pointers from the ends.

        Start with the widest possible container and shrink inward. Area is
        bounded by the shorter of the two walls, so moving the taller pointer
        can never help - the width only drops while the limiting height stays.
        Advancing the shorter wall is the only move that can find a taller
        limit, so it's always safe to discard it. O(n), single pass.
        """
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
