from typing import List


class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        # f[v][d] = longest subseq ending at value v with last abs-diff exactly d
        # but d can be 0..max(nums); we keep g[v][d] = best for last diff >= d
        M = max(nums) + 1
        # f[v][d] best length ending with value v and last diff exactly d
        # transition: f[v][d] = max over u with |v-u| == d of f[u][d'] for d' >= d, plus 1
        # use g[v][d] = max over d' >= d of f[v][d']
        f = [[0] * (M + 1) for _ in range(M)]
        g = [[0] * (M + 2) for _ in range(M)]
        ans = 1
        for x in nums:
            new_f_x = [0] * (M + 1)
            for d in range(M + 1):
                u1 = x - d
                u2 = x + d
                best = 0
                if 0 <= u1 < M:
                    best = max(best, g[u1][d])
                if 0 <= u2 < M and u2 != u1:
                    best = max(best, g[u2][d])
                new_f_x[d] = best + 1
            # merge into f and rebuild g[x]
            for d in range(M + 1):
                if new_f_x[d] > f[x][d]:
                    f[x][d] = new_f_x[d]
            # rebuild g[x] suffix max
            running = 0
            for d in range(M, -1, -1):
                if f[x][d] > running:
                    running = f[x][d]
                g[x][d] = running
            if g[x][0] > ans:
                ans = g[x][0]
        return ans

# refactored: cleaned up 3409
