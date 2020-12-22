# 235. Lowest Common Ancestor of a Binary Search Tree

Difficulty: Medium
Topics  : tree, dfs, binary search tree

## Problem

Given a BST and two nodes find their lowest common ancestor.

## Approach

Walk down. If both values are smaller go left, both larger go right, otherwise current node splits them and is the LCA.

## Complexity

Time O(h), space O(1).

## Files

- `python/solution.py`
