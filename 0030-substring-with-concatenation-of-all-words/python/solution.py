from typing import List
from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not words or not s:
            return []
        wlen = len(words[0])
        wcount = len(words)
        total = wlen * wcount
        target = Counter(words)
        result: List[int] = []
        n = len(s)
        for offset in range(wlen):
            left = offset
            window: Counter = Counter()
            count = 0
            for right in range(offset, n - wlen + 1, wlen):
                w = s[right:right + wlen]
                if w not in target:
                    window.clear()
                    count = 0
                    left = right + wlen
                    continue
                window[w] += 1
                count += 1
                while window[w] > target[w]:
                    lw = s[left:left + wlen]
                    window[lw] -= 1
                    count -= 1
                    left += wlen
                if count == wcount:
                    result.append(left)
        return result
