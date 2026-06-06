# 202. Happy Number

Difficulty: Easy
Topics: hash table, math, two pointers, cycle detection

## Problem

Starting from a positive integer n, repeatedly replace it with the sum of the squares of its digits. The number is happy if this process reaches 1; otherwise it loops forever in a cycle that never includes 1. Return whether n is happy.

## Approach

The sequence of "sum of digit squares" values is eventually periodic, so the question is really cycle detection. Use Floyd's tortoise and hare: advance one pointer by one step and the other by two. If the fast pointer reaches 1 the number is happy; if the pointers meet first we are in a cycle.

## Complexity

Time O(log n) per step with a bounded number of steps, space O(1).

## Files

- `python/solution.py`
