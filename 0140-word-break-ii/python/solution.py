from typing import List, Dict
from functools import lru_cache

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)

        @lru_cache(maxsize=None)
        def helper(i: int) -> List[str]:
            if i == len(s):
                return [""]
            out: List[str] = []
            for j in range(i + 1, len(s) + 1):
                w = s[i:j]
                if w in words:
                    for tail in helper(j):
                        out.append(w + (" " + tail if tail else ""))
            return out
        return helper(0)
