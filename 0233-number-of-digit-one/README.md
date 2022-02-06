# 233. Number of Digit One

Difficulty: Hard
Topics  : math, dp

## Problem

Count digit ones appearing in all non-negative integers <= n.

## Approach

Per-digit contribution. For each place value m, count how many ones land in that place.

## Complexity

Time O(log N), space O(1).

## Files

- `python/solution.py`
