from typing import List, Dict

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        memo: Dict[str, List[int]] = {}

        def helper(expr: str) -> List[int]:
            if expr in memo:
                return memo[expr]
            out: List[int] = []
            for i, ch in enumerate(expr):
                if ch in "+-*":
                    left = helper(expr[:i])
                    right = helper(expr[i + 1:])
                    for a in left:
                        for b in right:
                            if ch == "+":
                                out.append(a + b)
                            elif ch == "-":
                                out.append(a - b)
                            else:
                                out.append(a * b)
            if not out:
                out.append(int(expr))
            memo[expr] = out
            return out
        return helper(expression)
# ok
