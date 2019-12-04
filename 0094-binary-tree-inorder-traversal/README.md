# 94. Binary Tree Inorder Traversal

Difficulty: Easy
Topics: tree, dfs, stack

## Problem

Return the inorder traversal of a binary tree (left, root, right) as a list.

## Approach

Recursive: visit left, append root, visit right. Iterative: use a stack and walk left first.

## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
