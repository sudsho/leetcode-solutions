from typing import List
from collections import defaultdict

class Solution:
    def distinctNames(self, ideas: List[str]) -> int:
        groups: dict[str, set[str]] = defaultdict(set)
        for w in ideas:
            groups[w[0]].add(w[1:])
        keys = list(groups.keys())
        ans = 0
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = groups[keys[i]], groups[keys[j]]
                inter = len(a & b)
                ans += 2 * (len(a) - inter) * (len(b) - inter)
        return ans
