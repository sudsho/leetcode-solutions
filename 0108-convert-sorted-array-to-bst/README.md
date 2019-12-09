# 108. Convert Sorted Array to Binary Search Tree

Difficulty: Easy
Topics: tree, divide and conquer

## Problem

Given a sorted array, build a height-balanced BST.

## Approach

Pick the middle as root. Recurse on left half for left subtree, right half for right subtree.

## Complexity

Time O(n), space O(log n).

## Files

- `python/solution.py`
