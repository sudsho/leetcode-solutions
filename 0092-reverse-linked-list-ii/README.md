# 92. Reverse Linked List II

Difficulty: Medium
Topics  : linked list

## Problem

Reverse the nodes between positions left and right (1-indexed) in a singly linked list.

## Approach

Walk to position left-1. Reverse the segment in place by inserting each next node at the front.

## Complexity

Time O(N), space O(1).

## Files

- `python/solution.py`
