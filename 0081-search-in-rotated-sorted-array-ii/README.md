# 81. Search in Rotated Sorted Array II

Difficulty: Medium
Topics  : binary search

## Problem

Search a target in a rotated sorted array that may have duplicates.

## Approach

Modified binary search. When nums[lo] == nums[mid] == nums[hi], shrink both ends.

## Complexity

Time worst case O(N), space O(1).

## Files

- `python/solution.py`
