# 363. Max Sum of Rectangle No Larger Than k

Difficulty: Hard
Topics  : dp, binary search

## Problem

Max sum of a submatrix not larger than k.

## Approach

Iterate row pairs, compress to 1D, find max subarray sum <= k via sorted prefix sums.

## Complexity

Time O(R^2 * C log C), space O(C).

## Files

- `python/solution.py`
