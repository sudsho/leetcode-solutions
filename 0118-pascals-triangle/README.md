# 118. Pascal's Triangle

Difficulty: Easy
Topics  : array, dp

## Problem

Return the first numRows of Pascal's triangle. Each entry is the sum of the two above it.

## Approach

Build row by row. The endpoints are always 1, the interior j uses the previous row at j-1 and j. Initializing with `[1] * (i + 1)` lets the inner loop skip the borders entirely.

## Complexity

Time O(numRows^2), space O(numRows^2) for the output.

## Files

- `python/solution.py`
