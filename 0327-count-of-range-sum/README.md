# 327. Count of Range Sum

Difficulty: Hard
Topics  : merge sort, BIT

## Problem

Count number of (i, j) such that prefix[j] - prefix[i] is in [lower, upper].

## Approach

Merge sort over prefix sums. During merge count valid windows.

## Complexity

Time O(N log N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
