# 378. Kth Smallest Element In Sorted Matrix

Difficulty: Medium
Topics  : matrix, heap, binary search

## Problem

Kth smallest in an n by n row+col sorted matrix.

## Approach

Min-heap with first column, pop k-1 times pushing the next col cell.

## Complexity

Time O(k log n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`

<!-- revisit -->
