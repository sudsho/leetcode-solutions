# 107. Binary Tree Level Order Traversal II

Difficulty: Medium
Topics: tree, bfs, binary-tree

## Problem

Given the root of a binary tree, return the bottom-up level order traversal of
its node values - the values level by level, but with the leaf-most level first
and the root level last.

## Approach

Ordinary breadth-first traversal by levels, reversed once at the end. The level
batching is the standard trick: at the top of each iteration, capture
`len(queue)` so the inner loop pops exactly the nodes belonging to the current
level before any of their children (queued during the loop) are processed.

The only twist over the top-down version (problem 102) is the output order, and
the cleanest way to get it is to build the levels top-down and `reverse()` the
list of levels once. Prepending each level to the front instead would make every
insert O(L) and the whole thing O(L^2); a single reverse at the end is O(L).

## Complexity

Time O(n) - each node is enqueued and dequeued once - plus an O(L) reverse over
the L levels. Space O(n) for the output and O(w) for the queue, where w is the
widest level.

## Files

- `python/solution.py`
