# 337. House Robber III

Difficulty: Medium
Topics: tree, dynamic programming, depth-first search

## Problem

Houses form a binary tree. The root is the entrance and each node holds an amount
of money. The police are alerted if two directly-linked houses are robbed on the
same night. Return the maximum amount that can be robbed without alerting them.

## Approach

Bottom-up tree DP. Each node returns a pair: the best total if we rob this node,
and the best total if we skip it. Robbing a node forces both children to be
skipped, so `rob = val + skip(left) + skip(right)`. Skipping a node lets each
child take its own best, so `skip = max(child) summed over the two children`.
The answer is the larger of the two values returned by the root.

## Complexity

Time O(n), one pass over the tree. Space O(h) for the recursion stack, where h is
the tree height.

## Files

- `python/solution.py`
