# 272. Closest Binary Search Tree Value II

Difficulty: Hard
Topics  : tree, heap

## Problem

Find k values in a BST closest to a target.

## Approach

Inorder traversal with a sliding window of size k. Pop from front when adding to back yields a closer value.

## Complexity

Time O(N), space O(N).

## Files

- `python/solution.py`
- `python/solution_alt.py`
