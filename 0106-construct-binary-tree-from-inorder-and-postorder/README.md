# 106. Construct Binary Tree from Inorder and Postorder Traversal

Difficulty: Medium
Topics  : tree, hash table, divide and conquer

## Problem

Given inorder and postorder traversal arrays, reconstruct the binary tree.

## Approach

Last element of postorder is the root. Find it in inorder. Left part of inorder is the left subtree, right part is the right subtree. Consume postorder from the back, building the right subtree before the left since that is the order roots appear in reverse postorder. Hash the inorder indices for O(1) lookup.

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
