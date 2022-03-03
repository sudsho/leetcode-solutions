# 1591. Strange Printer II

Difficulty: Hard
Topics  : graph, topological sort

## Problem

Decide if a printer that can only print solid rectangles can produce the target grid.

## Approach

For each color, find its bounding rectangle. Within the rectangle, every other color seen must be painted later (edge). Toposort.

## Complexity

Time O(C * RC), space O(C^2).

## Files

- `python/solution.py`
