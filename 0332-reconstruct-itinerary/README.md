# 332. Reconstruct Itinerary

Difficulty: Hard
Topics  : graph, dfs, eulerian path, heap

## Problem

Reconstruct an itinerary from JFK using all tickets, lex-smallest.

## Approach

Hierholzer's algorithm. Use a min-heap per node, dfs and append on the way back.

## Complexity

Time O(E log E), space O(E).

## Files

- `python/solution.py`
- `python/solution_alt.py`
