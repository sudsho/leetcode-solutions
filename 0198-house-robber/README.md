# 198. House Robber

Difficulty: Easy
Topics: dynamic programming

## Problem

Given a list of house values along a street, compute the max amount you can rob without robbing two adjacent houses.

## Approach

At house i, best = max(best without i, best up to i-2 plus value[i]). Use two rolling variables.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
