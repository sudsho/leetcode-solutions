# 142. Linked List Cycle II

Difficulty: Medium
Topics  : linked list, two pointers

## Problem

Given a linked list return the node where the cycle begins, or None.

## Approach

Floyd's: detect with slow/fast, then walk one ptr from head and one from meeting point at same speed.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
