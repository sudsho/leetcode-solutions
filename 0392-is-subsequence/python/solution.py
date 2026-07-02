class Solution:
    def isSubsequence(self, s, t):
        """Check whether s is a subsequence of t with a two-pointer walk.

        Advance i through s only when the current s-char matches the current
        t-char; always advance j through t. If i reaches the end of s we found
        every char of s in order, so it is a subsequence.
        """
        i, j = 0, 0
        n, m = len(s), len(t)
        while i < n and j < m:
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == n
