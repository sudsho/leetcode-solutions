# 518. Coin Change 2

Difficulty: Medium
Topics  : dp, unbounded knapsack

## Problem

Number of ways to make amount with unlimited coins.

## Approach

Outer loop coins, inner loop amount. dp[a] += dp[a-coin].

## Complexity

Time O(amount * len(coins)), space O(amount).

## Files

- `python/solution.py`
- `python/solution_alt.py`
