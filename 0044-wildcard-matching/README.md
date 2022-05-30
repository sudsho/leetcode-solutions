# 44. Wildcard Matching

Difficulty: Hard
Topics  : dp, greedy

## Problem

Implement wildcard matching with `?` and `*`. `?` matches any single char. `*` matches any sequence including empty.

## Approach

Bottom up dp on (i, j). dp[i][j] true if s[:i] matches p[:j].

## Complexity

Time O(NM), space O(NM).

## Files

- `python/solution.py`
- `python/solution_alt.py`
