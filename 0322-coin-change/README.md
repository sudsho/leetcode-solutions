# 322. Coin Change

Difficulty: Medium
Topics  : array, dynamic programming, bfs

## Problem

Given coins and an amount return the fewest number of coins to make that amount, or -1 if impossible.

## Approach

1D dp[i] = min coins for amount i. Transition: try every coin.

## Complexity

Time O(amount * n), space O(amount).

## Files

- `python/solution.py`
- `python/solution_alt.py`
