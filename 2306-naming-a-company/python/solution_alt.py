from typing import List
from collections import defaultdict

class Solution:
    def distinctNames(self, ideas: List[str]) -> int:
        # for each suffix, collect the set of initial letters it appears with
        suffix_to_initials: dict[str, int] = defaultdict(int)
        for w in ideas:
            suffix_to_initials[w[1:]] |= 1 << (ord(w[0]) - ord('a'))
        # count per initial
        initial_total = [0] * 26
        # cnt[a][b] = number of suffixes with both initials a and b
        cnt = [[0] * 26 for _ in range(26)]
        for w in ideas:
            initial_total[ord(w[0]) - ord('a')] += 1
        for mask in suffix_to_initials.values():
            bits = [b for b in range(26) if mask & (1 << b)]
            for a in bits:
                for b in bits:
                    if a != b:
                        cnt[a][b] += 1
        ans = 0
        for a in range(26):
            for b in range(a + 1, 26):
                # ideas of a not containing b's suffix * ideas of b not containing a's suffix
                ans += 2 * (initial_total[a] - cnt[a][b]) * (initial_total[b] - cnt[b][a])
        return ans
