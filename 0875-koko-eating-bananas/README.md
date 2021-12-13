# 875. Koko Eating Bananas

Difficulty: Medium
Topics  : binary search, greedy

## Problem

Min eating speed to finish all piles in h hours.

## Approach

Binary search on speed. Time at speed k = sum(ceil(p/k)).

## Complexity

Time O(n log max), space O(1).

## Files

- `python/solution.py`
