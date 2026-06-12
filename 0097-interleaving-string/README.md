# 97. Interleaving String

Difficulty: Hard
Topics: string, dynamic programming

## Problem

Given strings s1, s2, and s3, return true if s3 is formed by an interleaving of
s1 and s2 - the characters of each are kept in order, and merged together.

## Approach

2-D DP collapsed to one row. dp[j] tracks whether the first i chars of s1 and
the first j chars of s2 can build the first i+j chars of s3. Reach a cell by
matching either the next s1 char (value from the previous row) or the next s2
char (value from the left).

## Complexity

Time O(m*n), space O(n).

## Files

- `python/solution.py`
