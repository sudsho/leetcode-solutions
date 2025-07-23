# 743. Network Delay Time

Difficulty: Medium
Topics  : graph, dijkstra, heap

## Problem

Min time for all nodes to receive a signal from k.

## Approach

Dijkstra from k. Answer is max distance, or -1 if unreachable.

## Complexity

Time O((V+E) log V), space O(V+E).

## Files

- `python/solution.py`
- `python/solution_alt.py`
