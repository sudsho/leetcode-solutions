# 89. Gray Code

Difficulty: Medium
Topics: bit manipulation, math

## Problem

Return any valid n-bit Gray code sequence of length `2^n` starting with 0, where consecutive entries differ in exactly one bit and the last and first also differ in one bit.

## Approach

The reflected binary gray code has a closed form: the i-th value is `i XOR (i >> 1)`. Walk `i` from `0` to `2^n - 1` and emit that value.

## Complexity

Time O(2^n), space O(1) extra.

## Files

- `python/solution.py`
