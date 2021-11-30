# 279. Perfect Squares

Difficulty: Medium
Topics  : dp, bfs, math

## Problem

Min number of perfect squares summing to n.

## Approach

Bottom-up DP. dp[i] = 1 + min(dp[i - k*k]) for k*k <= i.

## Complexity

Time O(n*sqrt(n)), space O(n).

## Files

- `python/solution.py`
