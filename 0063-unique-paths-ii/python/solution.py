class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid):
        """Count paths from top-left to bottom-right moving only down or right,
        where cells holding a 1 are blocked. Roll a single row of DP values
        across the grid: dp[c] is the number of ways to reach the current cell
        in column c. A blocked cell contributes zero ways; otherwise it adds the
        paths coming from above (the old dp[c]) and from the left (dp[c-1])."""
        if not obstacleGrid or not obstacleGrid[0]:
            return 0

        cols = len(obstacleGrid[0])
        dp = [0] * cols
        # the start cell seeds the count, unless it is itself an obstacle
        dp[0] = 1 if obstacleGrid[0][0] == 0 else 0

        for r, row in enumerate(obstacleGrid):
            for c, cell in enumerate(row):
                if cell == 1:
                    dp[c] = 0          # no path can pass through an obstacle
                elif c > 0:
                    dp[c] += dp[c - 1]  # paths from above already sit in dp[c]
                # c == 0 keeps whatever came from the row above (paths from top)

        return dp[-1]


if __name__ == "__main__":
    s = Solution()
    # one obstacle in the middle of a 3x3 grid -> 2 paths
    print(s.uniquePathsWithObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))  # 2
    # blocked start -> 0 paths
    print(s.uniquePathsWithObstacles([[1]]))  # 0
    # single open cell -> 1 path
    print(s.uniquePathsWithObstacles([[0]]))  # 1
