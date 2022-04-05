# 132. Palindrome Partitioning II

Difficulty: Hard
Topics  : dp

## Problem

Min cuts to partition s such that every substring is a palindrome.

## Approach

Compute palindrome 2D table. Then dp[i] = min cuts in s[:i+1].

## Complexity

Time O(N^2), space O(N^2).

## Files

- `python/solution.py`
- `python/solution_alt.py`
