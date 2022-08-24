from typing import List

class Solution:
    def removeInvalidParentheses(self, s: str) -> List[str]:
        result: List[str] = []
        l = r = 0
        for ch in s:
            if ch == "(":
                l += 1
            elif ch == ")":
                if l:
                    l -= 1
                else:
                    r += 1

        def valid(t: str) -> bool:
            bal = 0
            for ch in t:
                if ch == "(":
                    bal += 1
                elif ch == ")":
                    bal -= 1
                if bal < 0:
                    return False
            return bal == 0

        def backtrack(i: int, t: str, l_rem: int, r_rem: int) -> None:
            if i == len(s):
                if l_rem == 0 and r_rem == 0 and valid(t):
                    result.append(t)
                return
            ch = s[i]
            if ch == "(" and l_rem > 0 and (i == 0 or s[i - 1] != "("):
                backtrack(i + 1, t, l_rem - 1, r_rem)
            if ch == ")" and r_rem > 0 and (i == 0 or s[i - 1] != ")"):
                backtrack(i + 1, t, l_rem, r_rem - 1)
            backtrack(i + 1, t + ch, l_rem, r_rem)

        backtrack(0, "", l, r)
        return list(set(result))
