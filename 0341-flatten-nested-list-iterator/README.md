# 341. Flatten Nested List Iterator

Difficulty: Medium
Topics  : stack, design

## Problem

Iterator over a nested list of integers.

## Approach

Stack of iterators. Lazily descend into NestedInteger entries.

## Complexity

Time O(L) total, O(D) per next.

## Files

- `python/solution.py`
- `python/solution_alt.py`
