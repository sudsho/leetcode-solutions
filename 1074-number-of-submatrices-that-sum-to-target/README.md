# 1074. Number of Submatrices That Sum to Target

Difficulty: Hard
Topics  : array, matrix, hash table, prefix sum

## Problem

Given a 2D `matrix` and an integer `target`, count the number of non-empty submatrices whose elements sum to `target`. Two submatrices are different if they differ in position, even when their contents match.

## Approach

Brute force over all four boundaries is O(m^2 n^2) submatrices plus the cost of summing each, which is far too slow. The standard reduction is to fix a pair of column bounds and collapse the matrix down a dimension.

First build per-row prefix sums, so the sum of any horizontal run inside a row is one subtraction. Then for each column band `(c1, c2]`, collapse every row to its sum across that band. The band now reads as a 1D array, and "count submatrices summing to target" becomes "count subarrays summing to target" — which is 560 exactly. Sweep the rows with a running sum and a counter of previously seen prefix sums, adding `seen[running - target]` at each row.

Two details matter. The counter has to be seeded with `{0: 1}` so a submatrix starting at row 0 is counted, and it must be a *frequency* map rather than a set of first indices, because we want how many submatrices exist rather than the longest one. That is the same distinction that separates 560 from 525.

Counting is what forces the frequency map here. Rebuilding the counter fresh per band is also required, since prefix sums from one column band say nothing about another.

## Complexity

Let the matrix be m x n. Time O(n^2 m) for the column pairs times the row sweep, space O(mn) for the row-prefix table plus O(m) for the per-band counter.

## Files

- `python/solution.py`
