# 334. Increasing Triplet Subsequence

Difficulty: Medium
Topics: array, greedy

## Problem

Given an integer array `nums`, return `True` if there exists a triple of indices
`i < j < k` such that `nums[i] < nums[j] < nums[k]`, otherwise `False`.

## Approach

Greedily track two values: `first`, the smallest seen so far, and `second`, the
smallest value that has something strictly smaller before it. The first number
strictly greater than `second` completes an increasing triplet. Updating `first`
even after `second` is set is safe — `second` still encodes a real earlier pair.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
