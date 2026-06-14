class Solution:
    def kInversePairs(self, n, k):
        """Count arrays using 1..n exactly once that have exactly k inverse pairs.

        Let dp[i][j] be the number of such arrangements of i numbers with j
        inverse pairs. Inserting the largest of i numbers into a permutation of
        the smaller i-1 can create anywhere from 0 to i-1 new inverse pairs, so

            dp[i][j] = sum_{x=0}^{min(j, i-1)} dp[i-1][j-x].

        That inner sum is a sliding window over dp[i-1]; turning it into a prefix
        difference gives an O(1) step:

            dp[i][j] = dp[i][j-1] + dp[i-1][j] - dp[i-1][j-i]   (drop last term if j<i)

        We keep two rolling rows and work modulo 1e9+7.
        """
        MOD = 1_000_000_007
        prev = [0] * (k + 1)
        prev[0] = 1
        for i in range(1, n + 1):
            cur = [0] * (k + 1)
            cur[0] = 1
            for j in range(1, k + 1):
                cur[j] = (cur[j - 1] + prev[j]) % MOD
                if j - i >= 0:
                    cur[j] = (cur[j] - prev[j - i]) % MOD
            prev = cur
        return prev[k] % MOD
