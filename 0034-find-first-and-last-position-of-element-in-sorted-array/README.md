# 34. Find First And Last Position Of Element In Sorted Array

Difficulty: Medium
Topics  : array, binary search

## Problem

Given a sorted array `nums` and a `target`, return the indices of the first and last occurrence of `target`. Return `[-1, -1]` if not present. Must run in O(log n).

## Approach

Two binary searches: one for the leftmost insertion point of `target` (the first
index where `nums[i] >= target`), and one for the leftmost insertion point of
`target + 1` (then back off by 1 for the last occurrence). If the left bound
sits past the array or doesn't equal `target`, the value is missing.

Avoids the off-by-one mess of "search and then scan" by leaning on the standard
lower-bound primitive twice.

## Complexity

Time O(log n), space O(1).

## Files

- `python/solution.py`
