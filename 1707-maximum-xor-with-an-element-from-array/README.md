# 1707. Maximum Xor with an Element from Array

Difficulty: Hard
Topics  : trie, offline queries

## Problem

For each query (x, m) find the max value of x XOR a where a in nums and a <= m.

## Approach

Sort nums and queries. Build XOR trie incrementally; answer queries when threshold permits.

## Complexity

Time O((N + Q) log MAX), space O(N * 32).

## Files

- `python/solution.py`
