# 7. Reverse Integer

Difficulty: Easy
Topics  : math

## Problem

Given a 32-bit signed integer, reverse its digits. If the result overflows the 32-bit signed range, return 0.

## Approach

Pop digits off the end with mod 10 and push them onto a result. Keep track of the sign. Check for overflow at the end against 2^31 - 1 and -2^31.

<!-- updated -->
## Complexity

Time O(log10 x), space O(1).

## Files

- `python/solution.py`
