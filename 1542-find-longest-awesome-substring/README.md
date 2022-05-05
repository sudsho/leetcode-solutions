# 1542. Find Longest Awesome Substring

Difficulty: Hard
Topics  : bitmask, prefix

## Problem

Longest substring whose chars can be permuted to a palindrome (at most one odd count).

## Approach

Track bitmask parity of digits 0-9 over prefixes. At each position, look up earliest same mask, also masks differing by one bit.

## Complexity

Time O(N * 10), space O(2^10).

## Files

- `python/solution.py`
