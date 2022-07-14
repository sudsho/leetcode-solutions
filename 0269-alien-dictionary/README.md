# 269. Alien Dictionary

Difficulty: Hard
Topics  : graph, topological sort

## Problem

Given a sorted list of words from an alien alphabet, return the order of letters.

## Approach

Build precedence edges from adjacent word pairs at first differing char. Topo sort.

## Complexity

Time O(C), space O(1) for 26 letters.

## Files

- `python/solution.py`
