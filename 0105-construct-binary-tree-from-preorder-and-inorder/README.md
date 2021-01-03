# 105. Construct Binary Tree from Preorder and Inorder Traversal

Difficulty: Medium
Topics  : tree, hash table, divide and conquer

## Problem

Given preorder and inorder traversal arrays, reconstruct the binary tree.

## Approach

First element of preorder is the root. Find it in inorder. Left part of inorder is the left subtree, right part is the right subtree. Recurse. Use a hash to look up indices in O(1).

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
