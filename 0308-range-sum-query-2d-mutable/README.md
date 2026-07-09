# 308. Range Sum Query 2D - Mutable

Difficulty: Hard
Topics  : binary indexed tree, segment tree, matrix, design

## Problem

Given a 2D matrix, support two operations efficiently and interleaved:
- `update(row, col, val)` sets a single cell.
- `sumRegion(row1, col1, row2, col2)` returns the sum of a submatrix.

## Approach

Use a 2D Binary Indexed Tree (Fenwick tree). Each `update` pushes the delta
`val - old` along both axes in the usual `i += i & -i` fashion. A prefix query
sums the rectangle from the origin, and the answer for an arbitrary rectangle is
recovered by inclusion-exclusion over four prefix sums.

Keeping the raw cell values in a side array lets `update` compute the delta, so
repeated updates to the same cell stay correct.

## Complexity

Build O(m n log m log n), update and query O(log m log n), space O(m n).

## Files

- `python/solution.py`
