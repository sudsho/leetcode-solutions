# 261. Graph Valid Tree

Difficulty: Medium
Topics  : graph, union find, bfs

## Problem

Decide if an undirected edge list forms a tree.

## Approach

Tree iff exactly n-1 edges and a single connected component. Use union-find.

## Complexity

Time O(n + e * alpha), space O(n).

## Files

- `python/solution.py`
