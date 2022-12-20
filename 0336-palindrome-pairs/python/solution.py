from typing import List

class Solution:
    def palindromePairs(self, words: List[str]) -> List[List[int]]:
        index = {w: i for i, w in enumerate(words)}
        result: List[List[int]] = []
        for i, w in enumerate(words):
            for j in range(len(w) + 1):
                pre, suf = w[:j], w[j:]
                if pre == pre[::-1]:
                    rev = suf[::-1]
                    if rev != w and rev in index:
                        result.append([index[rev], i])
                if j != len(w) and suf == suf[::-1]:
                    rev = pre[::-1]
                    if rev != w and rev in index:
                        result.append([i, index[rev]])
        return result
