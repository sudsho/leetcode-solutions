# bit-by-bit common prefix walk
class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        result = 0
        for b in range(31, -1, -1):
            if (left >> b) != (right >> b):
                break
            result |= ((left >> b) & 1) << b
        return result
