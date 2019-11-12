# 700. Search in a Binary Search Tree

Difficulty: Easy
Topics: tree, binary search tree

## Problem

Given a BST and a value, return the subtree rooted at the matching node, else None.

## Approach

Walk down. At each node, go left or right based on comparison. Stop on match or null.

## Complexity

Time O(h), space O(1) iterative.

## Files

- `python/solution.py`
