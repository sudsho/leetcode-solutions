# alt: explicit two sums for readability

class Solution:
    def isBalanced(self, num: str) -> bool:
        even = sum(int(c) for i, c in enumerate(num) if i % 2 == 0)
        odd = sum(int(c) for i, c in enumerate(num) if i % 2 == 1)
        return even == odd
