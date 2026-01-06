from collections import Counter


class Solution:
    def countOfSubstrings(self, word: str, k: int) -> int:
        # at-least-k minus at-least-(k+1) trick
        def at_least(req: int) -> int:
            vowels_set = set("aeiou")
            cnt: Counter[str] = Counter()
            consonants = 0
            res = 0
            l = 0
            for r, ch in enumerate(word):
                if ch in vowels_set:
                    cnt[ch] += 1
                else:
                    consonants += 1
                while len(cnt) == 5 and consonants >= req:
                    res += len(word) - r
                    lch = word[l]
                    if lch in vowels_set:
                        cnt[lch] -= 1
                        if cnt[lch] == 0:
                            del cnt[lch]
                    else:
                        consonants -= 1
                    l += 1
            return res

        return at_least(k) - at_least(k + 1)
