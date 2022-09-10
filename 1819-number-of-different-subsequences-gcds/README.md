# 1819. Number of Different Subsequences Gcds

Difficulty: Hard
Topics  : math, harmonic enumeration

## Problem

Count distinct GCDs achievable from all non-empty subsequences of nums.

## Approach

For each candidate g in [1, max], take gcd of all multiples of g present. If equals g, count it.

## Complexity

Time O(M log M), space O(M).

## Files

- `python/solution.py`
- `python/solution_alt.py`
