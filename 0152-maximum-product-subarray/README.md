# 152. Maximum Product Subarray

Difficulty: Medium
Topics  : array, dynamic programming

## Problem

Find the contiguous subarray with the largest product.

## Approach

Track running max and min ending at each index (min matters because a negative*negative becomes large). Update both when we hit a negative.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
