# 219. Contains Duplicate II

Difficulty: Easy
Topics: array, hash table, sliding window

## Problem

Given nums and an integer k, return true if there are two distinct indices i and j such that nums[i] == nums[j] and abs(i - j) <= k.

## Approach

Walk once, storing each value's most recent index in a dict. On a repeat, the last stored index is the nearest one, so compare that gap to k before overwriting.

## Complexity

Time O(n), space O(min(n, k)) for the index map.

## Files

- `python/solution.py`
