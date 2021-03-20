# 33. Search in Rotated Sorted Array

Difficulty: Medium
Topics  : array, binary search

## Problem

Sorted array rotated at some pivot. Given a target return its index or -1. Must be O(log n).

## Approach

Modified binary search. Each iteration one half is sorted. Check which half is sorted, see if target lies inside it; otherwise go to the other half.

## Complexity

Time O(log n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
