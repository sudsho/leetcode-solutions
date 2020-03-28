# 448. Find All Numbers Disappeared in an Array

Difficulty: Easy
Topics: array, hash table

## Problem

Given nums of length n where each value is between 1 and n, return all values in [1, n] that do not appear in nums.

## Approach

Mark indices using sign flips. For each value v, negate nums[abs(v)-1]. Indices that remain positive are the missing values.

<!-- updated -->
## Complexity

Time O(n), space O(1) extra (output not counted).

## Files

- `python/solution.py`
