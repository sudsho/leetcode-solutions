# 42. Trapping Rain Water

Difficulty: Hard
Topics  : array, two pointers, stack, dp

## Problem

Compute total water trapped between bars.

## Approach

Two pointers from both ends, tracking left_max and right_max. The smaller side is the bottleneck.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
