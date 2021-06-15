from typing import List

class Solution:
    def findAllConcatenatedWordsInADict(self, words: List[str]) -> List[str]:
        words.sort(key=len)
        seen = set()
        out: List[str] = []
        for w in words:
            if not w:
                continue
            n = len(w)
            dp = [False] * (n + 1)
            dp[0] = True
            for i in range(1, n + 1):
                for j in range(0 if i == n else 1, i):
                    if dp[j] and w[j:i] in seen:
                        dp[i] = True
                        break
            if dp[n]:
                out.append(w)
            seen.add(w)
        return out
