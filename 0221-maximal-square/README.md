# 221. Maximal Square

Difficulty: Medium
Topics  : matrix, dp

## Problem

Largest square of 1s in a binary matrix.

## Approach

dp[i][j] = side of square ending at (i,j). dp = 1 + min(top, left, top-left) for 1 cells.

## Complexity

Time O(mn), space O(n).

## Files

- `python/solution.py`
