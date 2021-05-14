# 329. Longest Increasing Path In Matrix

Difficulty: Hard
Topics  : matrix, dp, dfs, memo

## Problem

Longest strictly increasing path in a matrix moving 4-dir.

## Approach

DFS with memo. cache[r][c] is the longest path starting from (r,c).

## Complexity

Time O(mn), space O(mn).

## Files

- `python/solution.py`
