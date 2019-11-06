# 617. Merge Two Binary Trees

Difficulty: Easy
Topics: tree, dfs

## Problem

Merge two binary trees by overlaying them. If two nodes overlap, the merged node value is the sum. If only one is present, use that one.

## Approach

Recurse. If either is null return the other. Else create a new node with sum and recurse on left/right pairs.

## Complexity

Time O(min(n,m)), space O(h).

## Files

- `python/solution.py`
