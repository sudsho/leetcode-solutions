# 129. Sum Root To Leaf Numbers

Difficulty: Medium
Topics  : tree + dfs

## Problem

Every root-to-leaf path forms a number by concatenating the node digits (root is the most significant digit). Return the sum of those numbers over all leaves.

## Approach

DFS carrying the prefix value. At each node the prefix grows to `prefix*10 + val`; contribute it to the sum only when the node is a leaf.

## Files

- `python/solution.py`
