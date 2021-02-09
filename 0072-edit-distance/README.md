# 72. Edit Distance

Difficulty: Hard
Topics  : string, dp

## Problem

Levenshtein distance between two strings.

## Approach

Classic 2D DP. dp[i][j] = ops to convert word1[:i] to word2[:j].

## Complexity

Time O(mn), space O(mn).

## Files

- `python/solution.py`
- `python/solution_alt.py`
