# 349. Intersection of Two Arrays

Difficulty: Easy
Topics  : array, hash table, two pointers, sorting

## Problem

Given two integer arrays, return their intersection. Each element in the result
must be unique and the order does not matter.

## Approach

Put each array in a set and take the set intersection with `&`. Because the
answer wants distinct values only, sets do the dedup for free. The alternate
file sorts both arrays and walks them with two pointers, advancing the smaller
side and recording a value once when they match - no extra set, at the cost of
the sort.

## Complexity

Set version: time O(n + m), space O(n + m). Two-pointer version: time
O(n log n + m log m) for the sort, space O(1) beyond the output.

## Files

- `python/solution.py`
- `python/solution_alt.py`
