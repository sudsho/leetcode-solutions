# 295. Find Median From Data Stream

Difficulty: Hard
Topics  : heap, design

## Problem

Add numbers and report the running median.

## Approach

Two heaps: max-heap of lower half, min-heap of upper half. Rebalance after each add.

## Complexity

Time O(log n) per add, O(1) for median.

## Files

- `python/solution.py`
- `python/solution_alt.py`
