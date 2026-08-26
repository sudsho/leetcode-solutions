# 2183. Count Array Pairs Divisible By K

Difficulty: Hard
Topics  : Number theory + counting by equivalence class

## Problem

Count index pairs `i < j` with `k | nums[i] * nums[j]`.

## Approach

The predicate factors through `x |-> gcd(x, k)`, so replace every element by its
class before counting anything. There are `d(k) <= 128` classes for `k <= 1e5`,
so the pair count is over classes rather than over elements: `O(n log k + d(k)^2)`.

## Files

- `python/solution.py`
