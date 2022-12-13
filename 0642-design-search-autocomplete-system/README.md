# 642. Design Search Autocomplete System

Difficulty: Hard
Topics  : trie, design

## Problem

Design an autocomplete: input chars one at a time, return top-3 by frequency.

## Approach

Trie with sentence counts at end nodes. On each char, walk to current node; collect descendants.

## Complexity

Time roughly O(L * S log S) per char.

## Files

- `python/solution.py`
- `python/solution_alt.py`
