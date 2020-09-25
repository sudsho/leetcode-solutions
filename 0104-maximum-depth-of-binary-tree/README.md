# 104. Maximum Depth of Binary Tree

Difficulty: Easy
Topics: tree, dfs

## Problem

Return the maximum depth (number of nodes along the longest root-to-leaf path) of a binary tree.

## Approach

Recurse. Depth of a node is 1 + max of depths of its children. Empty tree has depth 0.

<!-- updated -->
## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
