# 538. Convert BST to Greater Tree

Difficulty: Medium
Topics: binary search tree, depth-first search

## Problem

Convert a BST so every node's key becomes the original key plus the sum of all keys
greater than it. Return the modified root.

## Approach

Reverse in-order (right subtree, node, left subtree) visits keys from largest to
smallest. Carry a running sum: when we reach a node, the accumulator already holds the
total of every strictly greater key, so add the node's value and overwrite it in place.

## Complexity

Time O(n), space O(h) for the recursion stack.

## Files

- `python/solution.py`
