# 407. Trapping Rain Water II

Difficulty: Hard
Topics: heap, breadth-first search, matrix

## Problem

Given an `m x n` integer matrix of cell heights, compute the volume of water that can be trapped after raining. Water trapped on a cell is bounded by the lowest surrounding wall over any escape path to the border.

## Approach

Best-first flood fill from the border with a min-heap. Push all boundary cells, then repeatedly pop the lowest wall and visit its neighbours. A neighbour below the current wall level traps `wall - height` water; it is then pushed back at `max(wall, height)` since the effective barrier can only rise. Processing lowest-wall-first guarantees each cell is finalized by the true minimal enclosing wall.

## Complexity

Time O(mn log(mn)), space O(mn).

## Files

- `python/solution.py`
