# Group Anagrams (#49) - Medium
# Given an array of strings, group the anagrams together.
# Two strings are anagrams if they contain the same characters in any order.

from collections import defaultdict
from typing import List


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            # Use a 26-length tuple as the key - faster than sorting for long strings
            counts = [0] * 26
            for ch in s:
                counts[ord(ch) - ord('a')] += 1
            groups[tuple(counts)].append(s)
        return list(groups.values())


class SolutionSorted:
    """Alternative: use sorted string as the key. Simpler but O(k log k) per word."""
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strs:
            groups[tuple(sorted(s))].append(s)
        return list(groups.values())


if __name__ == "__main__":
    sol = Solution()
    print(sol.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    # [["eat","tea","ate"],["tan","nat"],["bat"]]
    print(sol.groupAnagrams([""]))    # [[""]]
    print(sol.groupAnagrams(["a"]))   # [["a"]]

# Time:  O(n * k) where n = len(strs), k = max word length
# Space: O(n * k)
