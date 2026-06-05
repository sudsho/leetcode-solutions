from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # Fixed-width sliding window of len(p). Keep a running count of the
        # window's chars and compare against p's count. Instead of comparing
        # the two 26-length tables every step, track how many letters are
        # currently "matched" (window count == target count) and only adjust
        # the two letters that change when the window slides.
        n, m = len(s), len(p)
        if m > n:
            return []

        need = [0] * 26
        window = [0] * 26
        for ch in p:
            need[ord(ch) - 97] += 1

        def idx(c: str) -> int:
            return ord(c) - 97

        matches = sum(1 for k in range(26) if need[k] == window[k])
        out = []
        for i in range(n):
            # add s[i] to the window
            r = idx(s[i])
            if window[r] == need[r]:
                matches -= 1
            window[r] += 1
            if window[r] == need[r]:
                matches += 1

            # drop the char that fell out of the left edge once full
            if i >= m:
                l = idx(s[i - m])
                if window[l] == need[l]:
                    matches -= 1
                window[l] -= 1
                if window[l] == need[l]:
                    matches += 1

            if matches == 26:
                out.append(i - m + 1)
        return out
