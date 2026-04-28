# First Unique Character in a String (#387) - Easy
# Given a string s, find the first non-repeating character and return its index.
# If it does not exist, return -1.

from collections import Counter


class Solution:
    def firstUniqChar(self, s: str) -> int:
        counts = Counter(s)
        for i, ch in enumerate(s):
            if counts[ch] == 1:
                return i
        return -1


if __name__ == "__main__":
    sol = Solution()
    print(sol.firstUniqChar("leetcode"))      # 0
    print(sol.firstUniqChar("loveleetcode"))  # 2
    print(sol.firstUniqChar("aabb"))          # -1

# Time:  O(n)
# Space: O(1) - bounded by alphabet size (26)
