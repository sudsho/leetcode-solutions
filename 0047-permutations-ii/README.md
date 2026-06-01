# 47. Permutations II

Difficulty: Medium
Topics  : backtracking, array

## Problem

Given a collection of numbers that may contain duplicates, return all possible unique permutations in any order.

## Approach

Sort first so duplicates sit next to each other. Standard backtracking with a `used[]` array. To skip duplicate branches: if the current value equals the previous and the previous slot is not currently in the path, skip — that branch was already covered when we placed the previous copy.

## Complexity

Time O(n * n!) worst case, space O(n) for the recursion path.

## Files

- `python/solution.py`
