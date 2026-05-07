# 110. Balanced Binary Tree

Difficulty: Easy
Topics  : tree, dfs, recursion

## Problem

Given a binary tree, decide whether it is height-balanced. A height-balanced tree is one in which the depths of the two subtrees of every node never differ by more than one.

## Approach

Recurse from the bottom up returning the height of each subtree, or a sentinel (-1) if any subtree below is already unbalanced. At each node compare left and right heights and bail out early as soon as the difference is greater than one. This avoids the O(n^2) cost of computing height separately for every node.

## Complexity

Time O(n), space O(h) for the recursion stack.

## Files

- `python/solution.py`
