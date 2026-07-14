# 225. Implement Stack using Queues

Difficulty: Easy
Topics: stack, queue, design

## Problem

Implement a last-in-first-out stack using only a queue's standard operations (push to back, pop from front, size, is empty). Support `push`, `pop`, `top`, and `empty`.

## Approach

Use one queue. On every `push`, append the new value, then move each older element from front to back so the freshly pushed value ends up at the front. Now `pop`/`top` just read the front. Push is O(n); the others are O(1).

## Complexity

Time O(n) push, O(1) pop/top/empty. Space O(n).

## Files

- `python/solution.py`
