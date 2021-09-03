# 787. Cheapest Flights Within K Stops

Difficulty: Medium
Topics  : graph, bellman ford, dp

## Problem

Cheapest src to dst with at most k stops.

## Approach

Bellman-Ford limited to k+1 relaxations.

## Complexity

Time O(k * E), space O(V).

## Files

- `python/solution.py`
