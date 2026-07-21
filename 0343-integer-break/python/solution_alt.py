class Solution:
    def integerBreak(self, n):
        """Bottom-up DP, the answer to reach for before spotting the 3s trick.

        dp[i] is the best product obtainable by breaking i into two or more
        parts. Build it up: for each i, try every first part j from 1..i-1 and
        pair it with the rest. The rest can be left whole (i - j) or itself be
        broken (dp[i - j]), so take the better of the two - that max() is what
        lets a "part" secretly be a further-broken chunk. The first factor stays
        a literal j because breaking i already guarantees the >= 2 parts rule.
        """
        dp = [0] * (n + 1)
        dp[1] = 1
        for i in range(2, n + 1):
            for j in range(1, i):
                dp[i] = max(dp[i], j * max(i - j, dp[i - j]))
        return dp[n]
