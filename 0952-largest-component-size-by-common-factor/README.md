# 952. Largest Component Size By Common Factor

Difficulty: Hard
Topics  : union find, math

## Problem

Largest connected component where edges link numbers sharing a common prime factor.

## Approach

Union-find. For each n, factor and union all primes dividing it.

## Complexity

Time O(N * sqrt(M)), space O(M).

## Files

- `python/solution.py`
