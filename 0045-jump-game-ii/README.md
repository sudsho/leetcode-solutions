# 45. Jump Game II

Difficulty: Medium
Topics  : greedy, dp

## Problem

Given an array where each element is the max jump length, return the minimum jumps to reach the last index.

## Approach

Greedy BFS-style: track current reach and farthest reachable; bump jumps when we exceed reach.

## Complexity

Time O(N), space O(1).

## Files

- `python/solution.py`
