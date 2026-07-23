# 701. Insert into a Binary Search Tree

Difficulty: Medium
Topics: binary search tree, recursion

## Problem

Given the root of a BST and a value, insert the value and return the root. The input is
guaranteed not to already contain the value; any valid resulting BST is accepted.

## Approach

Walk the BST invariant: go left when `val` is smaller, right otherwise, until falling off
the tree. That empty spot is exactly where `val` keeps the ordering, so attach a new leaf.
`solution.py` does this recursively; `solution_alt.py` is the iterative walk.

## Complexity

Time O(h) with h the tree height, space O(h) recursive / O(1) iterative.

## Files

- `python/solution.py`
- `python/solution_alt.py`
