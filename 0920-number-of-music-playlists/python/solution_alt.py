# rolling array dp, shaves space
class Solution:
    def numMusicPlaylists(self, n: int, goal: int, k: int) -> int:
        MOD = 10 ** 9 + 7
        prev = [0] * (n + 1)
        prev[0] = 1
        for i in range(1, goal + 1):
            curr = [0] * (n + 1)
            for j in range(1, n + 1):
                curr[j] = prev[j - 1] * (n - j + 1) % MOD
                if j > k:
                    curr[j] = (curr[j] + prev[j] * (j - k)) % MOD
            prev = curr
        return prev[n]
