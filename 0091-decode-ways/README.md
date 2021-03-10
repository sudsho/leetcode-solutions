# 91. Decode Ways

Difficulty: Medium
Topics  : string, dynamic programming

## Problem

Number of ways to decode a digit string into letters where 'A'=1..'Z'=26.

## Approach

1D dp. dp[i] = dp[i-1] (if s[i] is 1-9) + dp[i-2] (if s[i-1:i+1] is 10-26).

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
