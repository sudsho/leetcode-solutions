# 35. Search Insert Position

Difficulty: Easy
Topics  : binary search, array

## Problem

Given a sorted array and a target, return the index of the target if found, else the index where it would be inserted.

## Approach

Classic binary search. Maintain lo, hi range. When the loop exits, lo is the insertion point.

<!-- updated -->
## Complexity

Time O(log n), space O(1).

## Files

- `python/solution.py`
