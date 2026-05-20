# 40. Combination Sum II

Difficulty: Medium
Topics  : array, backtracking

## Problem

Given a collection of candidate numbers (which may contain duplicates) and a target, find all unique combinations where the candidates sum to target. Each candidate may be used at most once.

## Approach

Sort first so duplicates sit next to each other. Backtrack from `start`, and at each level skip an index whose value equals the previous one (only when `i > start`). The sort also lets us break early when the current value already exceeds the remaining target.

## Complexity

Time O(2^n) worst case, space O(n) for the recursion stack and path.

## Files

- `python/solution.py`
