# recursive divide and conquer
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def helper(b: float, e: int) -> float:
            if e == 0:
                return 1.0
            half = helper(b, e // 2)
            return half * half * (b if e % 2 else 1)
        if n < 0:
            return 1 / helper(x, -n)
        return helper(x, n)
