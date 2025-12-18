# 461. Hamming Distance

Difficulty: Easy
Topics: bit manipulation

## Problem

Hamming distance between two integers is the number of bit positions where they differ. Return that count.

## Approach

XOR the two numbers. Count the set bits in the result.

<!-- updated -->
## Complexity

Time O(1) (32 bits), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
