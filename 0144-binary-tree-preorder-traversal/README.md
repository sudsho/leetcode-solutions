# 144. Binary Tree Preorder Traversal

Difficulty: Easy
Topics: stack, tree, depth-first search, binary tree

## Problem

Given the root of a binary tree, return the preorder traversal of its nodes' values.

## Approach

Iterative DFS with an explicit stack. Pop a node, record its value, then push its right child before its left so the left subtree is processed first. The recursive version is a three-line root-left-right walk, but the stack form sidesteps recursion limits on degenerate (linked-list-shaped) trees.

## Complexity

Time O(n), space O(n) for the stack in the worst case.

## Files

- `python/solution.py`
