# 82. Remove Duplicates from Sorted List II

Difficulty: Medium
Topics: linked list, two pointers

## Problem

Given the head of a sorted linked list, delete all nodes that have duplicate numbers, leaving only distinct numbers from the original list. Return the linked list sorted as well.

## Approach

Single pass with a dummy head. Keep `prev` on the last confirmed-unique node. When the current node starts a run of equal values, walk to the end of that run and splice `prev.next` past it so the whole run is removed. The dummy node handles duplicate runs that begin at the head without extra cases.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
