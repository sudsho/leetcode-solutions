class Solution:
    def minimumTotal(self, triangle):
        """Minimum path sum from top to bottom, moving to adjacent indices.

        Work bottom-up: start from the last row and fold each row into the one
        above it. dp[j] = triangle[i][j] + min(dp[j], dp[j+1]). After folding
        every row the answer collapses into dp[0]. Reusing one array keeps the
        space at O(n) for the widest row.
        """
        dp = list(triangle[-1])
        for i in range(len(triangle) - 2, -1, -1):
            for j in range(len(triangle[i])):
                # from (i, j) the two legal steps land on (i+1, j) and (i+1, j+1),
                # which are exactly dp[j] and dp[j+1] in the row below
                dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
        return dp[0]
