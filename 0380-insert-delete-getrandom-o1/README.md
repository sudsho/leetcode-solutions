# 380. Insert Delete Getrandom O1

Difficulty: Medium
Topics  : design, hash map

## Problem

Implement RandomizedSet with insert, remove, getRandom in average O(1).

## Approach

Array of values plus dict mapping value -> index. Remove swaps last value into position.

## Complexity

Time O(1) average per op, space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
