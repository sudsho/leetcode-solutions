# 973. K Closest Points to Origin

Difficulty: Medium
Topics: array, heap, quickselect, divide and conquer

## Problem

Given an array of `points` on the plane and an integer `k`, return the `k`
points closest to the origin `(0, 0)`. Distance is standard Euclidean; the
answer may be returned in any order and is guaranteed unique.

## Approach

Compare squared distances `x*x + y*y` so we never touch a square root.

Two ways:

- **Max-heap of size k.** Push negated distances so the farthest of the
  current k is at the top; evict it whenever a closer point arrives.
  `O(n log k)` time, `O(k)` space - the natural choice for streaming or
  when `k << n`.
- **Quickselect.** Partition around a pivot distance until the k closest
  occupy the left slice. `O(n)` average, `O(n^2)` worst, in place.

## Complexity

Heap: time `O(n log k)`, space `O(k)`.
Quickselect: time `O(n)` average / `O(n^2)` worst, space `O(1)`.

## Files

- `python/solution.py`
