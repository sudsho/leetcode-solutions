# Longest Substring Without Repeating Characters
# Given a string s, find the length of the longest substring without
# repeating characters. Use a sliding window with a hash map.

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index = {}
        left = 0
        max_len = 0

        for right, char in enumerate(s):
            # if char was seen and is within current window, shrink left
            if char in char_index and char_index[char] >= left:
                left = char_index[char] + 1

            char_index[char] = right
            max_len = max(max_len, right - left + 1)

        return max_len


# Time complexity: O(n) — each character visited at most twice
# Space complexity: O(min(n, m)) where m is the character set size


if __name__ == "__main__":
    sol = Solution()

    assert sol.lengthOfLongestSubstring("abcabcbb") == 3   # "abc"
    assert sol.lengthOfLongestSubstring("bbbbb") == 1       # "b"
    assert sol.lengthOfLongestSubstring("pwwkew") == 3      # "wke"
    assert sol.lengthOfLongestSubstring("") == 0
    assert sol.lengthOfLongestSubstring("dvdf") == 3        # "vdf"

    print("all tests passed")
