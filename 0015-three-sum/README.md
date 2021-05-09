# 15. 3Sum

Difficulty: Medium
Topics: array, two pointers

## Problem

Given nums, find all unique triplets a, b, c such that a + b + c == 0. The result must not contain duplicate triplets.

## Approach

Sort. For each i, two-pointer scan over the rest looking for sum to -nums[i]. Skip duplicates at every level.

## Complexity

Time O(n^2), space O(1) extra (output not counted).

## Files

- `python/solution.py`
- `python/solution_alt.py`
