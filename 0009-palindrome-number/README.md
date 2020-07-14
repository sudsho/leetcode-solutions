# 9. Palindrome Number

Difficulty: Easy
Topics  : math

## Problem

Decide whether a given integer reads the same forward and backward. Negative numbers are never palindromes.

## Approach

Easiest is to convert to string and compare with its reverse. A more interesting math approach reverses half the number and compares to the other half.

<!-- updated -->
## Complexity

Time O(log10 x), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
