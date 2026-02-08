from typing import List
from collections import Counter


class Solution:
    def findCommonResponse(self, responses: List[List[str]]) -> str:
        cnt: Counter[str] = Counter()
        for row in responses:
            for w in set(row):
                cnt[w] += 1
        # most common, tie -> lex smallest
        best_word = ""
        best_count = -1
        for w, c in cnt.items():
            if c > best_count or (c == best_count and w < best_word):
                best_count = c
                best_word = w
        return best_word
