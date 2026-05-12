# 2. Add Two Numbers

Difficulty: Medium
Topics  : linked-list, math

## Problem

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each node contains a single digit. Add the two numbers and return the sum as a linked list.

## Approach

Because the least significant digit is at the head, we can walk both lists in lockstep and add digit-by-digit, propagating a carry. A dummy head keeps the tail-append logic clean and avoids a special case for the first node. The loop continues while either list still has nodes or there is a remaining carry (so an input like `9 + 1` correctly produces `1 -> 0`).

## Complexity

Time O(max(m, n)), space O(max(m, n)) for the result list.

## Files

- `python/solution.py`
