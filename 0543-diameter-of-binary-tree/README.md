# 543. Diameter of Binary Tree

Difficulty: Easy
Topics: tree, dfs

## Problem

Diameter is the number of edges on the longest path between any two nodes in a tree. Return the diameter.

## Approach

DFS that returns the depth of a subtree. At every node, candidate diameter is left depth + right depth. Track the max in a closure.

## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
