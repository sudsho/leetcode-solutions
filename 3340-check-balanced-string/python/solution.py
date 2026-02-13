class Solution:
    def isBalanced(self, num: str) -> bool:
        s = 0
        for i, ch in enumerate(num):
            s += int(ch) if i % 2 == 0 else -int(ch)
        return s == 0

# refactored: cleaned up 3340
