# 26. Remove Duplicates from Sorted Array

Difficulty: Easy
Topics: array, two pointers

## Problem

Modify a sorted array in place so that each element appears only once. Return the new length k. The first k elements should hold the unique values in order.

## Approach

Two pointers. Slow pointer marks the next slot for a unique value. Fast pointer scans. When fast finds a value different from arr[slow], advance slow and copy.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
