# 715. Range Module

Difficulty: Hard
Topics  : interval tree, sorted list

## Problem

Track ranges with addRange, queryRange, removeRange.

## Approach

Sorted list of disjoint intervals. Binary search to merge / split as needed.

## Complexity

Time O(log N) per op amortized.

## Files

- `python/solution.py`
- `python/solution_alt.py`
