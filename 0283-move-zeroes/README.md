# 283. Move Zeroes

Difficulty: Easy
Topics: array, two pointers

## Problem

Move all 0s in the array to the end while keeping the order of nonzero elements. Modify the array in place.

## Approach

Two pointers. Slow tracks the next slot for nonzero. Walk fast, when we see a nonzero copy to slow and increment. Then fill the rest with zeros.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
