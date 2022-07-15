from collections import Counter

class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        bulls = sum(s == g for s, g in zip(secret, guess))
        sc = Counter(secret)
        gc = Counter(guess)
        cows = sum((sc & gc).values()) - bulls
        return f"{bulls}A{cows}B"
# revised after retry
