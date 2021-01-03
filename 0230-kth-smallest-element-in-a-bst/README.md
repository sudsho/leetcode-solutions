# 230. Kth Smallest Element in a BST

Difficulty: Medium
Topics  : tree, dfs, binary search tree

## Problem

Given the root of a BST and an integer k return the kth smallest value (1-indexed).

## Approach

Iterative inorder with a stack. Pop k times.

## Complexity

Time O(h+k), space O(h).

## Files

- `python/solution.py`
- `python/solution_alt.py`
