# 450. Delete Node in a BST

Difficulty: Medium
Topics: binary search tree, recursion

## Problem

Given the root of a BST and a key, delete the node with that key (if present) and return
the new root, keeping the BST property.

## Approach

Recurse left/right by comparing key to the current node. Once found: with zero or one
child, return the surviving child to splice the node out. With two children, overwrite the
node's value with its in-order successor (leftmost node of the right subtree) and recurse
to delete that successor from the right subtree - it has at most one child, so it reduces
to an easier case.

## Complexity

Time O(h), space O(h) for the recursion, with h the tree height.

## Files

- `python/solution.py`
