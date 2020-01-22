# 100. Same Tree

Difficulty: Easy
Topics: tree, dfs

## Problem

Decide whether two binary trees are identical in both structure and values.

## Approach

Recurse. Both null = same. One null = different. Otherwise compare values and recurse on left and right children.

<!-- updated -->
## Complexity

Time O(n), space O(h) where h is height.

## Files

- `python/solution.py`
