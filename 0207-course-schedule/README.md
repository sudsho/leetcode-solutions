# 207. Course Schedule

Difficulty: Medium
Topics  : graph, dfs, bfs, topological sort

## Problem

Given numCourses and prerequisites, decide if you can finish all courses (i.e. the dependency graph has no cycle).

## Approach

Topological sort with Kahn's algorithm: repeatedly take nodes with in-degree zero. If we drain the graph we are good; otherwise a cycle exists.

## Complexity

Time O(V+E), space O(V+E).

## Files

- `python/solution.py`
