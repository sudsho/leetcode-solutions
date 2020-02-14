# 74. Search a 2D Matrix

Difficulty: Medium
Topics  : array, binary search, matrix

## Problem

Each row sorted, first element of each row > last of previous row. Search for target.

## Approach

Treat the matrix as a flat sorted array of length m*n; binary-search.

## Complexity

Time O(log(mn)), space O(1).

## Files

- `python/solution.py`
