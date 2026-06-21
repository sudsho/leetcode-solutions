# 203. Remove Linked List Elements

Difficulty: Easy
Topics: linked list

## Problem

Given the head of a linked list and an integer `val`, remove all the nodes of the linked list that have `Node.val == val`, and return the new head.

## Approach

Single pass with a dummy node in front of the head so that deletions at the very start need no special handling. Keep `prev` on the last node we decided to keep; when `cur` matches `val`, splice it out with `prev.next = cur.next` and leave `prev` where it is, otherwise advance `prev`. Return `dummy.next` since the head may have changed.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
