# 99. Recover Binary Search Tree

Difficulty: Medium
Topics  : tree, inorder

## Problem

Two nodes of a BST were swapped by mistake. Recover the tree without altering its structure.

## Approach

Inorder traversal yields a sequence with two violations (or one adjacent). Track first/second offending nodes, swap their values.

## Complexity

Time O(N), space O(H).

## Files

- `python/solution.py`
- `python/solution_alt.py`
