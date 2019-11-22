# 707. Design Linked List

Difficulty: Easy
Topics: linked list, design

## Problem

Implement a singly linked list with get(index), addAtHead(val), addAtTail(val), addAtIndex(index, val), deleteAtIndex(index).

## Approach

Hold a size counter and a sentinel head. Walk to index for get/insert/delete. Sentinel makes head insertion uniform.

## Complexity

Time O(n) per op in the worst case. Space O(n) overall.

## Files

- `python/solution.py`
