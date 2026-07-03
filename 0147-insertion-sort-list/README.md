# 147. Insertion Sort List

Difficulty: Medium
Topics: linked list, sorting

## Problem

Sort a singly-linked list using insertion sort and return the sorted list's head.

## Approach

Keep a dummy-headed sorted list. Pop each node from the input, scan the sorted part from the dummy to find the first slot whose next value exceeds it, and splice it in.

## Complexity

Time O(n^2) worst case, space O(1) (nodes are relinked, not copied).

## Files

- `python/solution.py`
