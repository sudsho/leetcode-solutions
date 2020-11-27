# 155. Min Stack

Difficulty: Easy
Topics: stack, design

## Problem

Design a stack that also supports getMin in O(1). All operations push, pop, top, getMin must run in constant time.

## Approach

Keep a parallel min stack. Each push also pushes the current min onto it. Top of min stack is always the current minimum.

<!-- revisited -->
## Complexity

All ops O(1).

## Files

- `python/solution.py`
