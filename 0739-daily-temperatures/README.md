# 739. Daily Temperatures

Difficulty: Medium
Topics  : array, stack, monotonic stack

## Problem

Given a list of daily temperatures, for each day return the number of days you'd have to wait until a warmer temperature.

## Approach

Monotonic decreasing stack of indices. When today is warmer than the top, pop and write the diff.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
