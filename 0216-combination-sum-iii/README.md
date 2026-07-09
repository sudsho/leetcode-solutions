# 216. Combination Sum III

Difficulty: Medium
Topics  : backtracking, combinations

## Problem

Find all combinations of `k` distinct numbers from 1..9 that add up to `n`.
Each number is used at most once and every combination must be unique.

## Approach

Backtrack over digits in increasing order, tracking the remaining target. Since
digits only increase along a branch, once the current digit exceeds the
remaining sum we can stop scanning. Record a combination when it holds exactly
`k` digits and the remaining target is zero.

## Complexity

Time O(C(9, k)) in the worst case, space O(k) for the recursion depth.

## Files

- `python/solution.py`
