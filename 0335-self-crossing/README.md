# 335. Self Crossing

Difficulty: Hard
Topics: math, geometry

## Problem

You move on a plane: `distance[0]` units north, `distance[1]` west,
`distance[2]` south, `distance[3]` east, and so on counter-clockwise. Return
whether the path ever crosses itself.

## Approach

A crossing can only happen against one of the previous few edges, giving exactly
three geometric cases: the spiral that tightens and crosses the edge 3 back, the
edge that exactly meets the one 4 back, and the wider crossing involving the edge
5 back. Check these for each step in O(1) space.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
