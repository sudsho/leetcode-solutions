# Given a string s, return the longest palindromic substring in s.
# A palindrome reads the same forward and backward.
# Approach: expand around each center (handles both odd and even length palindromes).


class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        start, end = 0, 0

        def expand(left: int, right: int) -> tuple[int, int]:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - 1

        for i in range(len(s)):
            l1, r1 = expand(i, i)
            l2, r2 = expand(i, i + 1)
            if r1 - l1 > end - start:
                start, end = l1, r1
            if r2 - l2 > end - start:
                start, end = l2, r2

        return s[start:end + 1]


if __name__ == "__main__":
    sol = Solution()
    print(sol.longestPalindrome("babad"))   # "bab" or "aba"
    print(sol.longestPalindrome("cbbd"))    # "bb"
    print(sol.longestPalindrome("a"))       # "a"

# Time: O(n^2) - for each center we expand up to n chars
# Space: O(1) - only constant extra space
