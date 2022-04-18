# 140. Word Break II

Difficulty: Hard
Topics  : dp, backtracking, memo

## Problem

Return all possible sentences formed by inserting spaces in s such that each fragment is in wordDict.

## Approach

Top-down memoization on suffix index. Reuse subresults across recursive calls.

## Complexity

Time exponential in worst case, space O(N * answers).

## Files

- `python/solution.py`
