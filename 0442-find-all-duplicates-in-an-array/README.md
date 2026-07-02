# 442. Find All Duplicates in an Array

Difficulty: Medium
Topics: array, hash table, in-place marking

## Problem

Given an integer array nums of length n where every value is in [1, n] and each value appears once or twice, return all values that appear twice. Do it in O(n) time and without extra space.

## Approach

Use the array itself as a seen-set. Value v belongs at index v-1, so negate nums[v-1] the first time v is visited. If that slot is already negative, v has been seen before, so it is a duplicate. Take absolute values while indexing since earlier steps may have flipped signs.

## Complexity

Time O(n), space O(1) extra (output not counted).

## Files

- `python/solution.py`
