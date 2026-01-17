from collections import defaultdict
from typing import DefaultDict


class Solution:
    def countOfSubstrings(self, word: str, k: int) -> int:
        vowels = set("aeiou")

        def at_least(req: int) -> int:
            vc: DefaultDict[str, int] = defaultdict(int)
            uniq = 0
            cons = 0
            res = 0
            l = 0
            for r in range(len(word)):
                c = word[r]
                if c in vowels:
                    if vc[c] == 0:
                        uniq += 1
                    vc[c] += 1
                else:
                    cons += 1
                while uniq == 5 and cons >= req:
                    res += len(word) - r
                    lc = word[l]
                    if lc in vowels:
                        vc[lc] -= 1
                        if vc[lc] == 0:
                            uniq -= 1
                    else:
                        cons -= 1
                    l += 1
            return res

        return at_least(k) - at_least(k + 1)
