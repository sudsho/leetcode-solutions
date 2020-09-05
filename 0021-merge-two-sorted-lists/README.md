# 21. Merge Two Sorted Lists

Difficulty: Easy
Topics  : linked list

## Problem

Given two sorted linked lists, merge them into one sorted linked list and return its head.

## Approach

Use a dummy head. Walk both lists, attach the smaller node to the tail, advance that list. When one runs out, attach the remainder of the other.

<!-- revisited -->
## Complexity

Time O(n + m), space O(1) extra (we reuse nodes).

## Files

- `python/solution.py`
