# 815. Bus Routes

Difficulty: Hard
Topics  : graph, bfs

## Problem

Min number of buses to take from source to target.

## Approach

BFS over routes. Map stop -> set of routes containing it. Visit routes once.

## Complexity

Time O(sum of route sizes), space O(sum of route sizes).

## Files

- `python/solution.py`
