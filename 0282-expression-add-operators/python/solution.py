from typing import List

class Solution:
    def addOperators(self, num: str, target: int) -> List[str]:
        result: List[str] = []

        def backtrack(i: int, expr: str, value: int, last: int) -> None:
            if i == len(num):
                if value == target:
                    result.append(expr)
                return
            for j in range(i + 1, len(num) + 1):
                part = num[i:j]
                if len(part) > 1 and part[0] == "0":
                    break
                n = int(part)
                if i == 0:
                    backtrack(j, part, n, n)
                else:
                    backtrack(j, expr + "+" + part, value + n, n)
                    backtrack(j, expr + "-" + part, value - n, -n)
                    backtrack(j, expr + "*" + part, value - last + last * n, last * n)
        backtrack(0, "", 0, 0)
        return result
