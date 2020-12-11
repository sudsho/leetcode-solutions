# 14. Longest Common Prefix

Difficulty: Easy
Topics: string

## Problem

Given a list of strings, return the longest prefix that all of them share. Return empty string if there is no common prefix.

## Approach

Take the first string as candidate and check character by character against every other string. Stop at the first mismatch.

<!-- updated -->
## Complexity

Time O(S) where S is sum of all chars. Space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
