# 112. Path Sum

Difficulty: Easy
Topics: tree, dfs, recursion

## Problem

Given the root of a binary tree and an integer targetSum, return true if the
tree has a root-to-leaf path such that adding up all the values along the path
equals targetSum.

## Approach

Recurse, subtracting the current node's value from the target as we descend.
At a leaf the path is valid iff the leftover target equals zero. Internal nodes
just OR together the two subtree results.

## Complexity

Time O(n), space O(h) for the recursion stack where h is tree height.

## Files

- `python/solution.py`
- `python/solution_alt.py` - iterative stack version carrying the running sum
