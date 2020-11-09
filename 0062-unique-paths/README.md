# 62. Unique Paths

Difficulty: Medium
Topics  : math, dynamic programming, combinatorics

## Problem

An m x n grid. Count unique paths from top-left to bottom-right moving only right or down.

## Approach

1D dp. Row by row, dp[j] becomes dp[j] + dp[j-1].

## Complexity

Time O(m*n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
