# 658. Find K Closest Elements

Difficulty: Medium
Topics  : array, binary search, two pointers

## Problem

Return k closest elements to x in a sorted array.

## Approach

Binary search on the left index of the window of size k.

## Complexity

Time O(log(n-k) + k), space O(k).

## Files

- `python/solution.py`
