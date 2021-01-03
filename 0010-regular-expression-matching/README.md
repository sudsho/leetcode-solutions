# 10. Regular Expression Matching

Difficulty: Hard
Topics  : string, dp, recursion

## Problem

Match a string s against a pattern p with `.` and `*`.

## Approach

2D DP. dp[i][j] is True iff s[:i] matches p[:j]. star handles zero or one-or-more matches.

## Complexity

Time O(mn), space O(mn).

## Files

- `python/solution.py`
- `python/solution_alt.py`
