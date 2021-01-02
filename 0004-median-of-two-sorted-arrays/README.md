# 4. Median Of Two Sorted Arrays

Difficulty: Hard
Topics  : array, binary search, divide and conquer

## Problem

Find median of two sorted arrays in O(log(min(m,n))).

## Approach

Binary search on partition of the smaller array so left halves combined have ceil((m+n)/2) elements.

## Complexity

Time O(log(min(m,n))), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
