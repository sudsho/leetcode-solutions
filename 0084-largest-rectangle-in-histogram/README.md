# 84. Largest Rectangle In Histogram

Difficulty: Hard
Topics  : stack, monotonic stack

## Problem

Largest rectangle area inside a histogram.

## Approach

Monotonic increasing stack of indices. On a smaller bar, pop and compute area with current i as right bound.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
