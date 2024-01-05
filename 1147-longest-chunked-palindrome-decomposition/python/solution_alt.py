class Solution:
    def longestDecomposition(self, text: str) -> int:
        # Recursive variant with prefix==suffix check
        def go(s: str) -> int:
            n = len(s)
            for k in range(1, n // 2 + 1):
                if s[:k] == s[-k:]:
                    return 2 + go(s[k:-k])
            return 1 if s else 0
        return go(text)
