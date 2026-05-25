# 103. Binary Tree Zigzag Level Order Traversal

Difficulty: Medium
Topics  : tree, bfs

## Problem

Given the root of a binary tree, return the zigzag level order traversal of its node values. Level 0 goes left to right, level 1 right to left, and so on, alternating between every level.

## Approach

Standard level-order BFS with a queue. For each level pop exactly `level_size` nodes so we know where the level ends. Collect the values in their natural left-to-right BFS order, then reverse the list in place on every other level before appending it to the answer. A boolean toggled each iteration tracks which direction the current level wants.

Reversing once per level is O(level_size) and cheaper than inserting at the front for every node, which would push us toward O(n^2) on skewed shapes.

## Complexity

Time O(n) since each node is enqueued and dequeued once and the per-level reverse is linear in the level's width. Space O(n) for the queue and the output structure.

## Files

- `python/solution.py`
