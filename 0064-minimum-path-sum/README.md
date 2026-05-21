# 64. Minimum Path Sum

Difficulty: Medium
Topics  : array, dynamic programming, matrix

## Problem

Given an `m x n` grid of non-negative integers, find a path from the top-left to the bottom-right that minimizes the sum of values along the path. You can only move right or down at any step.

## Approach

Classic grid DP. For any cell `(i, j)` the minimum path sum to reach it is `grid[i][j] + min(dp[i-1][j], dp[i][j-1])`, with the top row and left column being prefix sums.

Since each row only depends on the row above and the cell to its left in the current row, we collapse the 2D table into a single rolling row of length `n` and update it left to right.

## Complexity

Time O(m*n), space O(n).

## Files

- `python/solution.py`
