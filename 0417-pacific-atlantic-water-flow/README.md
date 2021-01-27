# 417. Pacific Atlantic Water Flow

Difficulty: Medium
Topics  : array, dfs, bfs, matrix

## Problem

Given a heights grid return cells from which water can flow to both Pacific (top/left edges) and Atlantic (bottom/right edges).

## Approach

Reverse the flow: BFS from each ocean inward (only ascending). Intersection of reachable sets is the answer.

## Complexity

Time O(m*n), space O(m*n).

## Files

- `python/solution.py`
- `python/solution_alt.py`
