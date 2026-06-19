class Solution:
    def restoreIpAddresses(self, s):
        """Return every valid IP address formable by inserting dots into `s`.

        Backtracking: place exactly four segments, each 1-3 characters. A segment
        is valid when it has no leading zero (unless it is exactly "0") and its
        integer value is at most 255. We prune early - if the remaining characters
        cannot possibly fill the segments still owed (too few or too many), we
        stop that branch instead of exploring it.
        """
        n = len(s)
        out = []

        def backtrack(start, segments):
            # Done when four segments are placed and the whole string is consumed.
            if len(segments) == 4:
                if start == n:
                    out.append(".".join(segments))
                return
            # Length pruning: each remaining segment holds 1..3 chars.
            remaining = 4 - len(segments)
            left = n - start
            if left < remaining or left > remaining * 3:
                return
            for size in range(1, 4):
                if start + size > n:
                    break
                piece = s[start:start + size]
                if (piece[0] == "0" and size > 1) or int(piece) > 255:
                    continue
                backtrack(start + size, segments + [piece])

        backtrack(0, [])
        return out
