from functools import lru_cache

class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        @lru_cache(maxsize=None)
        def go(i: int, mask: int, changed: int) -> int:
            if i == n:
                return 1
            best = 0
            for c in range(26):
                if c != ord(s[i]) - 97 and changed:
                    continue
                bit = 1 << c
                new_mask = mask | bit
                use_change = changed or (c != ord(s[i]) - 97)
                if bin(new_mask).count('1') > k:
                    best = max(best, 1 + go(i + 1, bit, use_change))
                else:
                    best = max(best, go(i + 1, new_mask, use_change))
            return best
        return go(0, 0, 0)
# minor cleanup
