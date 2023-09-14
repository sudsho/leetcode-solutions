# 2023 nit (164)
# bottom up, builds list per index
from typing import List, Dict

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        words = set(wordDict)
        max_len = max((len(w) for w in words), default=0)
        cache: Dict[int, List[str]] = {len(s): [""]}

        def helper(i: int) -> List[str]:
            if i in cache:
                return cache[i]
            res: List[str] = []
            for j in range(i + 1, min(len(s), i + max_len) + 1):
                w = s[i:j]
                if w in words:
                    for tail in helper(j):
                        res.append(w + (" " + tail if tail else ""))
            cache[i] = res
            return res
        return helper(0)
