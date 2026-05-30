# 16. 3Sum Closest

Difficulty: Medium
Topics  : array, two pointers, sorting

## Problem

Given an integer array and a target, find three integers in the array whose sum is closest to target. Return the sum.

## Approach

Sort the array, then for each anchor index `i`, sweep two pointers from `i+1` and `n-1`. Track the best sum by absolute distance to target. Move the pointer that drags the sum toward target (left if sum is too small, right if too big). Skip duplicate anchors to avoid redundant work. Exact hit returns early.

## Complexity

Time O(n^2), space O(1) extra (sort in place).

## Files

- `python/solution.py`
