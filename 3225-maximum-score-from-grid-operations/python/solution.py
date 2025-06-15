from typing import List

class Solution:
    def maximumScore(self, grid: List[List[int]]) -> int:
        n = len(grid)
        # column prefix sums
        col_pre = [[0] * (n + 1) for _ in range(n)]
        for c in range(n):
            for r in range(n):
                col_pre[c][r + 1] = col_pre[c][r] + grid[r][c]
        # dp[j][k] = max score for column c-1 with j blacks (top), considering c
        # State: previous column's bottom of black is at row j (0..n)
        NEG = -10 ** 18
        # dp_prev[j] = best score where prev column has black rows [0, j)
        # extend stride: we process columns; black per column is a prefix of size 0..n
        dp_prev = [0] * (n + 1)
        for c in range(1, n):
            dp_cur = [NEG] * (n + 1)
            # f[j] = best dp_prev[k] + (gain when prev col has k blacks and cur col has j blacks)
            # gain split into pieces depending on j vs k
            # Brute O(n^3) per column total O(n^4) — only ok for small n; use prefix tricks
            for j in range(n + 1):  # cur column blacks = top j rows
                # cur column contributes to scoring its non-black neighbors in prev column
                best = NEG
                for k in range(n + 1):  # prev column blacks
                    # prev's white rows that have black neighbor in cur (rows k..j-1) get scored if not already
                    # plus cur's white rows with black neighbor in prev
                    gain1 = (col_pre[c - 1][j] - col_pre[c - 1][min(j, k)]) if j > k else 0
                    gain2 = (col_pre[c][k] - col_pre[c][min(k, j)]) if k > j else 0
                    cand = dp_prev[k] + gain1 + gain2
                    if cand > best:
                        best = cand
                dp_cur[j] = best
            dp_prev = dp_cur
        return max(dp_prev)
