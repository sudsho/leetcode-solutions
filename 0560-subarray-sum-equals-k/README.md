# 560. Subarray Sum Equals K

Difficulty: Medium
Topics  : array, hash table, prefix sum

## Problem

Given an int array and integer k return the total number of contiguous subarrays whose sum equals k.

## Approach

Prefix-sum trick. Count how many times each prefix sum appeared; for each new prefix, look up (prefix - k).

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
