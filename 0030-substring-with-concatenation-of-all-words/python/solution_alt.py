# brute version: enumerate every starting index, count words
from typing import List
from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words:
            return []
        wlen = len(words[0])
        wcount = len(words)
        total = wlen * wcount
        target = Counter(words)
        result: List[int] = []
        for i in range(len(s) - total + 1):
            seen: Counter = Counter()
            for j in range(wcount):
                w = s[i + j * wlen:i + (j + 1) * wlen]
                if w not in target:
                    break
                seen[w] += 1
                if seen[w] > target[w]:
                    break
            else:
                result.append(i)
        return result
