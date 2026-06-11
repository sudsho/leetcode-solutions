class Solution:
    def countBits(self, n):
        """Return ans[0..n] where ans[i] is the popcount of i.

        Key recurrence: dropping the lowest bit of i gives i >> 1, which we
        have already solved, and the lowest bit itself contributes i & 1.
        So ans[i] = ans[i >> 1] + (i & 1), filled left to right in O(n).
        """
        ans = [0] * (n + 1)
        for i in range(1, n + 1):
            ans[i] = ans[i >> 1] + (i & 1)
        return ans
