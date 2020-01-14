# 28. Implement strStr()

Difficulty: Easy
Topics: string

## Problem

Find the first index where needle occurs in haystack, or return -1 if not found. If needle is empty return 0.

## Approach

Slide the needle along haystack. At each position compare the next len(needle) characters. Stop at first match.

<!-- updated -->
## Complexity

Time O(n*m) naive. Space O(1).

## Files

- `python/solution.py`
