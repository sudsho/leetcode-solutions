class Solution:
    def longestDupSubstring(self, s: str) -> str:
        MOD = (1 << 61) - 1
        BASE = 257
        n = len(s)
        nums = [ord(c) for c in s]

        def search(L: int) -> int:
            h = 0
            base_L = pow(BASE, L, MOD)
            for i in range(L):
                h = (h * BASE + nums[i]) % MOD
            seen = {h: [0]}
            for i in range(1, n - L + 1):
                h = (h * BASE - nums[i - 1] * base_L + nums[i + L - 1]) % MOD
                if h in seen:
                    cand = s[i:i + L]
                    for start in seen[h]:
                        if s[start:start + L] == cand:
                            return i
                    seen[h].append(i)
                else:
                    seen[h] = [i]
            return -1

        lo, hi = 1, n
        start, length = 0, 0
        while lo < hi:
            L = (lo + hi) // 2
            idx = search(L)
            if idx != -1:
                start = idx
                length = L
                lo = L + 1
            else:
                hi = L
        return s[start:start + length]
