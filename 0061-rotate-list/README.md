# 61. Rotate List

Difficulty: Medium
Topics: linked list, two pointers

## Problem

Given the head of a linked list, rotate the list to the right by k places. k can be larger than the length of the list.

## Approach

Walk the list once to find its length and tail, then reduce k modulo the length so we never rotate more than necessary. Close the list into a ring by pointing the tail at the head. The new tail is `length - k` steps from the original head; cut the ring just after it and return the node that follows as the new head.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
