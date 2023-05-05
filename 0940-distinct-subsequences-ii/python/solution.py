class Solution:
    def distinctSubseqII(self, s: str) -> int:
        MOD = 10 ** 9 + 7
        last: dict[str, int] = {}
        dp = [0]  # dp[0] = 1 (empty)
        dp[0] = 1
        for i, c in enumerate(s, 1):
            cur = dp[-1] * 2 % MOD
            if c in last:
                cur = (cur - dp[last[c] - 1]) % MOD
            dp.append(cur)
            last[c] = i
        return (dp[-1] - 1) % MOD
