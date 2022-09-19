# 154. Find Minimum in Rotated Sorted Array II

Difficulty: Hard
Topics  : binary search

## Problem

Find the minimum in a rotated sorted array that may contain duplicates.

## Approach

Binary search on (lo, hi). Compare nums[mid] to nums[hi]; on equality, decrement hi.

## Complexity

Time avg O(log N), worst O(N), space O(1).

## Files

- `python/solution.py`
