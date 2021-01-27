# 139. Word Break

Difficulty: Medium
Topics  : string, dynamic programming, hash table

## Problem

Given a string s and a dictionary, return True if s can be segmented into words from the dict.

## Approach

1D dp where dp[i] = True if s[:i] is segmentable. For each i, look back for a j with dp[j] True and s[j:i] in dict.

## Complexity

Time O(n^2 * k) worst, space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
