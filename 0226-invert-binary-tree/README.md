# 226. Invert Binary Tree

Difficulty: Easy
Topics: tree, dfs

## Problem

Invert (mirror) a binary tree by swapping left and right children of every node.

## Approach

Recurse. Swap children, then recurse into them. Or do BFS/DFS and swap as you visit.

<!-- updated -->
## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
