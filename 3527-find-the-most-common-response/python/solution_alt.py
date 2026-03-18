# alt: sort approach

from typing import List
from collections import Counter


class Solution:
    def findCommonResponse(self, responses: List[List[str]]) -> str:
        cnt: Counter[str] = Counter()
        for row in responses:
            for w in set(row):
                cnt[w] += 1
        items = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))
        return items[0][0]
