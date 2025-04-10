# 210. Course Schedule Ii

Difficulty: Medium
Topics  : graph, topo sort

## Problem

Return an order to take all courses given prerequisites.

## Approach

Kahn's BFS. Build indegree, queue zero-indegree, pop and decrement.

## Complexity

Time O(V + E), space O(V + E).

## Files

- `python/solution.py`
- `python/solution_alt.py`
