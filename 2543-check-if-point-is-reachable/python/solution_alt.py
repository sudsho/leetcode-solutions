from math import gcd

class Solution:
    def isReachable(self, targetX: int, targetY: int) -> bool:
        g = gcd(targetX, targetY)
        return (g & (g - 1)) == 0

# revisit: minor renames and one early exit added
