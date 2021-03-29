# 39. Combination Sum

Difficulty: Medium
Topics  : array, backtracking

## Problem

Given distinct positive ints and a target, return all unique combinations that sum to target. Each number can be used unlimited times.

## Approach

Backtracking. Sort first to prune. At each step either include the current candidate (and stay on it, since reuse allowed) or move on.

## Complexity

Time exponential in worst case, space O(target).

## Files

- `python/solution.py`

<!-- revisit -->
- `python/solution_alt.py`
