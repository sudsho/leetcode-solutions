class Solution:
    def longestDecomposition(self, text: str) -> int:
        n = len(text)
        i, j = 0, n - 1
        count = 0
        left = right = ""
        while i <= j:
            left += text[i]
            right = text[j] + right
            if left == right:
                count += 1
                left = right = ""
            i += 1
            j -= 1
        if left:
            count += 1
        return count
# corrected edge case
# tightened naming
# refactored helper
# style tweak
# minor cleanup
# small fix
# tightened naming (more)
