# 18. 4Sum

Difficulty: Medium
Topics: array, two pointers

## Problem

Given an array of integers `nums` and a target, return all unique quadruplets `[a, b, c, d]` such that `a + b + c + d == target`.

## Approach

Sort the array. Two outer loops fix the first two elements, then run a two-pointer scan for the remaining pair sum. Skip duplicates at every level, and prune with min/max window checks so we bail out early on hopeless prefixes.

## Complexity

Time O(n^3), space O(1) extra (output not counted).

## Files

- `python/solution.py`
