# 1235. Maximum Profit Job Scheduling

Difficulty: Hard
Topics  : dp, binary search

## Problem

Pick non-overlapping jobs to maximize total profit.

## Approach

Sort by end. dp[i] = max(dp[i-1], profit[i] + dp[index of last non-conflicting]).

## Complexity

Time O(n log n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
