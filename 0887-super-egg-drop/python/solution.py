class Solution:
    def superEggDrop(self, k: int, n: int) -> int:
        # f[m][k] = max floors covered with m moves and k eggs
        f = [[0] * (k + 1) for _ in range(n + 1)]
        m = 0
        while f[m][k] < n:
            m += 1
            for j in range(1, k + 1):
                f[m][j] = 1 + f[m - 1][j - 1] + f[m - 1][j]
        return m
# refactored helper
# tightened naming
