# 77. Combinations

Difficulty: Medium
Topics: backtracking

## Problem

Return all possible combinations of `k` numbers chosen from the range `[1, n]`.

## Approach

Backtracking with a `start` cursor so each combination is generated in increasing order (no duplicates by construction). Prune the inner range: once we still need `r = k - len(path)` more numbers, the largest valid starting index is `n - r + 1`.

## Complexity

Time O(C(n, k) * k) to enumerate and copy each combination. Recursion depth up to k.

## Files

- `python/solution.py`
