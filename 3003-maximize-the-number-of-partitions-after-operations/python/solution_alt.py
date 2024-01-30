from functools import lru_cache

class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        # Two-pass DP: forward partitions[i], backward, then try changing each char
        n = len(s)
        if n == 0:
            return 0
        # forward: partitions[i] = (#partitions ending before i, mask after i, distinct chars in current group at i)
        # Brute n*26 = 26n calls of an inner partition-count function; small data
        def base_partitions(t: str) -> int:
            cnt = 1
            mask = 0
            for ch in t:
                bit = 1 << (ord(ch) - 97)
                new_mask = mask | bit
                if bin(new_mask).count('1') > k:
                    cnt += 1
                    mask = bit
                else:
                    mask = new_mask
            return cnt
        best = base_partitions(s)
        for i in range(n):
            for c in range(26):
                if c == ord(s[i]) - 97:
                    continue
                modified = s[:i] + chr(c + 97) + s[i + 1:]
                v = base_partitions(modified)
                if v > best:
                    best = v
        return best
