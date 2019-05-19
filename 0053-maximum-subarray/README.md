# 53. Maximum Subarray

Difficulty: Easy
Topics: dynamic programming, array

## Problem

Given an integer array, find the contiguous subarray with the largest sum and return that sum. The array can have negative numbers.

## Approach

Kadane: at each index keep the best sum that ends here. Either extend the previous run or start over at the current value. Track global max along the way.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
