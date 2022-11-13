# 305. Number of Islands II

Difficulty: Hard
Topics  : union find

## Problem

After each addLand operation in an m x n grid, return the count of islands.

## Approach

Union-find on grid index. New land becomes its own component, then unions with neighboring lands.

## Complexity

Time O(K * inv-Ackermann), space O(MN).

## Files

- `python/solution.py`
- `python/solution_alt.py`
