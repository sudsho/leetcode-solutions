# 1463. Cherry Pickup II

Difficulty: Hard
Topics  : dp

## Problem

Two robots from top corners pick cherries; max cherries collected.

## Approach

DP on (row, c1, c2). Each step, both robots move to one of {-1, 0, +1} columns.

## Complexity

Time O(R * C^2 * 9), space O(R * C^2).

## Files

- `python/solution.py`
