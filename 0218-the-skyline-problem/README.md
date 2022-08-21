# 218. The Skyline Problem

Difficulty: Hard
Topics  : heap, sweep line

## Problem

Given building rectangles, output the skyline as a list of key points.

## Approach

Process events (left/right edges) in order. Max-heap of active heights with lazy removal.

## Complexity

Time O(N log N), space O(N).

## Files

- `python/solution.py`
