# 95. Unique Binary Search Trees II

Difficulty: Medium
Topics  : tree, dp, recursion

## Problem

Generate all structurally unique BSTs storing values 1..n.

## Approach

Pick each i as root; left subtrees from build(lo, i-1), right from build(i+1, hi). Cross product.

## Complexity

Time roughly Catalan, space same.

## Files

- `python/solution.py`
