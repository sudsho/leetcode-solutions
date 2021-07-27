# 437. Path Sum III

Difficulty: Medium
Topics  : tree, dfs, hash table, prefix sum

## Problem

Given a binary tree and an integer target return the number of paths whose values sum to target. Paths must go top-down but can start and end anywhere.

## Approach

DFS with a running prefix-sum count. Number of valid paths ending at the current node is the count of (prefix - target).

## Complexity

Time O(n), space O(n).

## Files

- `python/solution.py`
- `python/solution_alt.py`

<!-- revisit -->
