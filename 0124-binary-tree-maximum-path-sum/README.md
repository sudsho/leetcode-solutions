# 124. Binary Tree Maximum Path Sum

Difficulty: Hard
Topics  : tree, dfs, dynamic programming

## Problem

Given a binary tree return the maximum path sum, where a path is any sequence of nodes connected by edges.

## Approach

DFS returns the max gain extending from this node downward (one branch). At each node consider the case where path bends through it: left+node+right.

## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
