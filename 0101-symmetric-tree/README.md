# 101. Symmetric Tree

Difficulty: Easy
Topics: tree, dfs

## Problem

Decide if a binary tree is a mirror of itself. Left subtree should be the mirror of right subtree.

## Approach

Helper that takes two nodes and compares them as mirror images: a.left vs b.right, a.right vs b.left.

## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
