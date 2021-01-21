# 55. Jump Game

Difficulty: Medium
Topics  : array, greedy, dynamic programming

## Problem

Each element is the max jump length from that position. Determine if you can reach the last index.

## Approach

Greedy. Track the farthest index reachable so far; iterate. If we ever stand on an index past it we cannot continue.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
