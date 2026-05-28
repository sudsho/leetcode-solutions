# 191. Number of 1 Bits

Difficulty: Easy
Topics  : bit manipulation

## Problem

Count the number of set bits in the binary representation of an unsigned integer.

## Approach

The straightforward way is to shift and mask with `& 1` for each of the 32 bits. The nicer trick is Brian Kernighan's: `n & (n - 1)` always clears the lowest set bit, so the loop runs once per 1-bit instead of 32 times.

## Complexity

Time O(k) where k is the number of set bits, space O(1).

## Files

- `python/solution.py`
