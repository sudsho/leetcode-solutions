# 240. Search a 2D Matrix II

Difficulty: Medium
Topics  : array, binary search, divide and conquer, matrix

## Problem

Search for target in an m x n matrix where each row and each column is sorted ascending.

## Approach

Start at top-right. Larger goes left, smaller goes down.

## Complexity

Time O(m+n), space O(1).

## Files

- `python/solution.py`
