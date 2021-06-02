# 162. Find Peak Element

Difficulty: Medium
Topics  : array, binary search

## Problem

Find any peak in O(log n).

## Approach

Binary search: if nums[mid] < nums[mid+1] go right, else go left.

## Complexity

Time O(log n), space O(1).

## Files

- `python/solution.py`

<!-- revisit -->
