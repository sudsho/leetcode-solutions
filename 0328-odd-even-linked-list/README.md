# 328. Odd Even Linked List

Difficulty: Medium
Topics: linked list

## Problem

Given the head of a singly linked list, group all nodes with odd indices together followed by the nodes with even indices, and return the reordered list. Indices are 1-based. Solve in O(1) extra space and O(n) time, keeping the relative order within each group.

## Approach

Walk two pointers down the list at once. `odd` chains the 1st, 3rd, 5th... nodes and `even` chains the 2nd, 4th... . Save the even head first so once both walks finish we can hang the even sublist off the odd tail. Loop while `even` and `even.next` are both live.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
