# 63. Unique Paths II

Difficulty: Medium
Topics: dynamic programming, array

## Problem

Given an `m x n` grid where some cells contain obstacles (marked 1), count the number of distinct paths from the top-left to the bottom-right corner. You can only move down or right, and you cannot step on an obstacle.

## Approach

Same grid DP as Unique Paths, but obstacles zero out a cell's path count. Keep a single rolling row `dp` where `dp[c]` is the number of ways to reach the current cell in column c. For each cell, an obstacle resets it to 0; otherwise add the paths coming from the left (`dp[c-1]`) to the paths already stored from the row above (`dp[c]`). Seed `dp[0]` with 1 unless the start cell is blocked.

## Complexity

Time O(m*n), space O(n).

## Files

- `python/solution.py`
