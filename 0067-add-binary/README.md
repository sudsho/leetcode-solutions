# 67. Add Binary

Difficulty: Easy
Topics: string, math

## Problem

Given two binary strings a and b, return their sum as a binary string.

## Approach

Walk both strings from the right with a carry. Build the result digit by digit, then reverse it.

<!-- updated -->
## Complexity

Time O(max(n,m)), space O(max(n,m)).

## Files

- `python/solution.py`
