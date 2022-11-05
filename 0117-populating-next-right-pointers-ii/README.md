# 117. Populating Next Right Pointers II

Difficulty: Medium
Topics  : tree, bfs

## Problem

Connect each node to its next right node. Tree is not perfect.

## Approach

Use the already-built next pointers on the parent level to walk and stitch the child level.

## Complexity

Time O(N), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
