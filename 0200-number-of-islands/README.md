# 200. Number of Islands

Difficulty: Medium
Topics  : array, dfs, bfs, matrix, union find

## Problem

Given a 2D grid of '1' (land) and '0' (water), return the number of connected land components.

## Approach

DFS or BFS from each unvisited land cell, sinking visited cells.

## Complexity

Time O(m*n), space O(m*n) recursion.

## Files

- `python/solution.py`
