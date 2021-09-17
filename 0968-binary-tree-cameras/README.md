# 968. Binary Tree Cameras

Difficulty: Hard
Topics  : tree, dp, greedy

## Problem

Min cameras to monitor every node in a binary tree.

## Approach

Post-order DFS with 3 states: covered-with-camera, covered-without, uncovered. Greedy place at parent when child uncovered.

## Complexity

Time O(n), space O(h).

## Files

- `python/solution.py`
