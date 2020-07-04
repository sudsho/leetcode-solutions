# 994. Rotting Oranges

Difficulty: Medium
Topics  : array, bfs, matrix

## Problem

BFS through an oranges grid: 0 empty, 1 fresh, 2 rotten. Each minute rotten infects 4-neighbors. Return minutes until all rotten or -1.

## Approach

Multi-source BFS from all initial rotten cells. Track minutes by level.

## Complexity

Time O(m*n), space O(m*n).

## Files

- `python/solution.py`
