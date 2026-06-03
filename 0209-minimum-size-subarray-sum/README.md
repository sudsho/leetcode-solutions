# 209. Minimum Size Subarray Sum

Difficulty: Medium
Topics: array, sliding window, prefix sum, binary search

## Problem

Given an array of positive integers and a target, return the minimal length of a contiguous subarray whose sum is >= target. Return 0 if none exists.

## Approach

Two pointer sliding window. Expand the right edge adding to the running sum; whenever the sum reaches the target, record the window length and shrink from the left. Because all values are positive, shrinking only ever lowers the sum, so the window stays valid to test.

## Complexity

Time O(n), space O(1). The alt prefix-sum + binary search version is O(n log n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
