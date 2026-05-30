# 69. Sqrt(x)

Difficulty: Easy
Topics  : binary search, math

## Problem

Return the integer square root of a non-negative integer x (floor of the real square root).

## Approach

Binary search for the largest k where k*k <= x. Upper bound is x/2 + 1, which is safe for any x >= 2; small inputs (0, 1) are handled directly. Comparing k*k vs x is cleaner than dividing and dodges the zero edge case.

## Complexity

Time O(log x), space O(1).

## Files

- `python/solution.py`
