# 1293. Shortest Path With Obstacle Elimination

Difficulty: Hard
Topics  : matrix, bfs

## Problem

Shortest path from corner to corner allowed to remove up to k obstacles.

## Approach

BFS on (r, c, k_left). Track visited per remaining k.

## Complexity

Time O(m * n * k), space O(m * n * k).

## Files

- `python/solution.py`
