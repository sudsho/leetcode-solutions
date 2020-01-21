# 300. Longest Increasing Subsequence

Difficulty: Medium
Topics  : array, dynamic programming, binary search

## Problem

Given an int array return the length of the longest strictly increasing subsequence.

## Approach

n^2 dp is straightforward; faster O(n log n) uses patience-sorting style: maintain tails of growing piles, and binary-search the slot for each new element.

## Complexity

Time O(n log n), space O(n).

## Files

- `python/solution.py`
