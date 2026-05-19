# 29. Divide Two Integers

Difficulty: Medium
Topics  : math, bit manipulation

## Problem

Divide two integers without using multiplication, division, or the mod operator. Return the quotient truncated toward zero. The environment is 32-bit signed, so clamp to [-2^31, 2^31 - 1].

## Approach

Work with absolute values and track the sign separately. To divide a by b, repeatedly find the largest k such that `b << k <= a`, subtract `b << k` from a, and add `1 << k` to the result. Doubling b until it would overshoot a is essentially doing long division in binary.

The only overflow case to special-case is `INT_MIN / -1`, which we return as `INT_MAX`.

## Complexity

The outer loop runs O(log(a/b)) times, and each iteration finds the right shift in O(log(a/b)) work, so O(log^2 N) overall.

## Files

- `python/solution.py`
