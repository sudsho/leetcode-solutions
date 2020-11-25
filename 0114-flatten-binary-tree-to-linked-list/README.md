# 114. Flatten Binary Tree to Linked List

Difficulty: Medium
Topics  : tree, dfs, stack

## Problem

Flatten a binary tree to a right-linked-list following preorder, in place.

## Approach

For each node with a left child, find the rightmost node in the left subtree and stitch the original right subtree onto it; then move left to right and clear left.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
