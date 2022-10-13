# 109. Convert Sorted List to Binary Search Tree

Difficulty: Medium
Topics  : tree, linked list

## Problem

Convert a sorted singly linked list to a height-balanced BST.

## Approach

Two pass: count length, then in-order build using mutable index walking the list.

## Complexity

Time O(N), space O(log N).

## Files

- `python/solution.py`
