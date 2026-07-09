# 190. Reverse Bits

Difficulty: Easy
Topics  : bit manipulation, divide and conquer

## Problem

Reverse the bits of a given 32-bit unsigned integer.

## Approach

Read the low bit of `n` and shift it into the result from the left, 32 times.
The first bit read lands in the top position, the last in the bottom, which is
exactly the reversal.

If the function is called repeatedly, reverse a byte at a time using a 256-entry
lookup table so each word costs four table hits instead of 32 iterations.

## Complexity

Time O(1) (fixed 32 bits), space O(1); the table variant is O(256) preprocessing.

## Files

- `python/solution.py`
