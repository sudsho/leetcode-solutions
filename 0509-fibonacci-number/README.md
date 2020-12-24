# 509. Fibonacci Number

Difficulty: Easy
Topics: dynamic programming, math

## Problem

Compute the nth Fibonacci number, where F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2).

## Approach

Iterate with two rolling variables. Avoid the exponential blow-up of naive recursion.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
