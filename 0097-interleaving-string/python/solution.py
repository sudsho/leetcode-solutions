class Solution:
    def isInterleave(self, s1, s2, s3):
        """Return True if s3 is formed by interleaving s1 and s2.

        DP over a 1-D row. dp[j] answers "can s1[:i] and s2[:j] interleave to
        form s3[:i+j]?" as we sweep i from 0..m. Each cell can be reached either
        by consuming a char of s1 (dp[j] from the row above) or a char of s2
        (dp[j-1] in the current row).
        """
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False

        dp = [False] * (n + 1)
        dp[0] = True
        for j in range(1, n + 1):
            dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

        for i in range(1, m + 1):
            dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
            for j in range(1, n + 1):
                from_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
                from_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
                dp[j] = from_s1 or from_s2
        return dp[n]
