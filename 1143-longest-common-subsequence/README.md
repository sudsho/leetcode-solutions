# 1143. Longest Common Subsequence

Difficulty: Medium
Topics  : string, dp

## Problem

LCS of two strings.

## Approach

2D DP. Match increases, mismatch takes max of two neighbors.

## Complexity

Time O(mn), space O(min(m,n)).

## Files

- `python/solution.py`
- `python/solution_alt.py`
