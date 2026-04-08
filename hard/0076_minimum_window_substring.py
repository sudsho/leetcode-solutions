# Given strings s and t, return the minimum window substring of s such that
# every character in t (including duplicates) is included in the window.
# Return empty string "" if no such window exists.

from collections import Counter


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not t or not s:
            return ""

        need = Counter(t)
        missing = len(t)  # total characters still needed in window
        best_left, best_right = 0, float("inf")
        left = 0

        for right, char in enumerate(s):
            # Expand window: absorb char from right
            if need[char] > 0:
                missing -= 1
            need[char] -= 1

            # Window is valid — try to contract from left
            if missing == 0:
                # Move left pointer past characters not needed
                while need[s[left]] < 0:
                    need[s[left]] += 1
                    left += 1

                # Update best window if this one is smaller
                if right - left < best_right - best_left:
                    best_left, best_right = left, right

                # Break the window by removing leftmost needed char
                need[s[left]] += 1
                missing += 1
                left += 1

        return "" if best_right == float("inf") else s[best_left: best_right + 1]


# Time:  O(|s| + |t|) — each character visited at most twice (left + right pointers)
# Space: O(|s| + |t|) — Counter dictionaries for character frequencies

if __name__ == "__main__":
    sol = Solution()

    # Classic example
    assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"

    # t longer than s
    assert sol.minWindow("a", "aa") == ""

    # Exact match
    assert sol.minWindow("a", "a") == "a"

    # Duplicates in t
    assert sol.minWindow("aa", "aa") == "aa"

    print("All test cases passed.")
