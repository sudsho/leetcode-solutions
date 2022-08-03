# explicit two-pass counting
class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        bulls = 0
        cs = [0] * 10
        cg = [0] * 10
        for s, g in zip(secret, guess):
            if s == g:
                bulls += 1
            else:
                cs[int(s)] += 1
                cg[int(g)] += 1
        cows = sum(min(cs[i], cg[i]) for i in range(10))
        return f"{bulls}A{cows}B"
