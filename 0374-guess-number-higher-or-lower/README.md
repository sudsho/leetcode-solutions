# 374. Guess Number Higher or Lower

Difficulty: Easy
Topics: binary search, interactive

## Problem

We pick a number from 1 to n. Repeatedly call the `guess(num)` API, which returns
-1 if `num` is higher than the pick, 1 if lower, and 0 on a match. Return the pick.

## Approach

Binary search on the answer. Keep a `[lo, hi]` window and probe the midpoint; the
sign returned by `guess` says which half to keep. Converges in about log2(n) calls.

## Complexity

Time O(log n), space O(1).

## Files

- `python/solution.py`
