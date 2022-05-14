# 173. Binary Search Tree Iterator

Difficulty: Medium
Topics  : tree, design

## Problem

Iterator over a BST exposing next() and hasNext() in average O(1).

## Approach

Stack of left spines. On next, pop, push right child's left spine.

## Complexity

Time O(1) amortized per call, space O(H).

## Files

- `python/solution.py`
