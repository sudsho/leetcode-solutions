# 119. Pascal's Triangle II

Difficulty: Easy
Topics: array, dynamic programming

## Problem

Given an integer rowIndex, return the rowIndex-th (0-indexed) row of Pascal's triangle.

## Approach

Grow a single list row by row. For each step append a trailing 1, then update the interior entries right-to-left so each becomes the sum of itself and its left neighbour. Right-to-left avoids overwriting a value before it is read.

## Complexity

Time O(rowIndex^2), space O(rowIndex) for the one row we keep.

## Files

- `python/solution.py`
