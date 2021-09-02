# 778. Swim In Rising Water

Difficulty: Hard
Topics  : matrix, heap, binary search, union find

## Problem

Min time t such that you can walk from (0,0) to (n-1,n-1) only on cells with value <= t.

## Approach

Dijkstra-flavored: min-heap of (height, r, c). Final answer is max height encountered on the path.

## Complexity

Time O(n^2 log n), space O(n^2).

## Files

- `python/solution.py`
