# 987. Vertical Order Traversal of a Binary Tree

Difficulty: Hard
Topics: binary tree, depth-first search, hash table, sorting

## Problem

Assign each node a (row, col): root is (0, 0), a left child is (row+1, col-1), a right
child is (row+1, col+1). Report values column by column left to right; within a column
order by row top to bottom, and when two nodes share the same row and column order them
by value (ascending).

## Approach

One traversal tagging every node with its (row, col), bucketed by column into a hash map.
The tie-break rule is the catch: two nodes can land on the same (row, col), so sorting a
column by `(row, value)` handles both the top-to-bottom order and the same-cell value tie
in one pass. Emit columns in sorted key order.

## Complexity

Time O(n log n) dominated by the per-column sorts, space O(n).

## Files

- `python/solution.py`
