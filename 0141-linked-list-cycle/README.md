# 141. Linked List Cycle

Difficulty: Easy
Topics: linked list, two pointers

## Problem

Decide whether a singly linked list has a cycle.

## Approach

Floyd two-pointer (tortoise and hare). Slow moves one, fast moves two. If they ever meet there is a cycle. If fast hits None there is none.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
