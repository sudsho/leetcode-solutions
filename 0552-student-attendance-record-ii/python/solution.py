class Solution:
    def checkRecord(self, n: int) -> int:
        MOD = 10 ** 9 + 7
        # dp[a][l] where a in {0,1}, l in {0,1,2}
        dp = [[0, 0, 0], [0, 0, 0]]
        dp[0][0] = 1
        for _ in range(n):
            new = [[0, 0, 0], [0, 0, 0]]
            for a in range(2):
                for l in range(3):
                    v = dp[a][l]
                    if not v:
                        continue
                    new[a][0] = (new[a][0] + v) % MOD  # P
                    if a == 0:
                        new[1][0] = (new[1][0] + v) % MOD  # A
                    if l < 2:
                        new[a][l + 1] = (new[a][l + 1] + v) % MOD  # L
            dp = new
        return sum(sum(row) for row in dp) % MOD
