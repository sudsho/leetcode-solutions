# 111. Minimum Depth of Binary Tree

Difficulty: Easy
Topics: tree, bfs, dfs, binary-tree

## Problem

Given a binary tree, return its minimum depth: the number of nodes along the
shortest path from the root down to the nearest leaf. A leaf is a node with no
children.

## Approach

Breadth-first search, returning the depth of the first leaf encountered. The
trap here is the leaf definition: a node with a single child must keep going
down that one child, so the tempting `1 + min(minDepth(left), minDepth(right))`
recurrence is wrong whenever one side is empty - it reports depth 1 for a path
that has not actually reached a leaf. BFS avoids special-casing that: it visits
nodes in nondecreasing depth order, so the very first childless node it pops is
the shallowest leaf in the tree, and we return its depth immediately.

A DFS works too, but then the one-child case has to be handled explicitly
(recurse only into the non-empty side); BFS gets the early exit for free.

## Complexity

Time O(n) worst case, but BFS stops as soon as it finds a leaf, so a shallow
leaf is reported without touching the rest of the tree. Space O(w) for the
queue, where w is the maximum width of a level.

## Files

- `python/solution.py`
