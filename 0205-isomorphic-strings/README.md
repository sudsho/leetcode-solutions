# 205. Isomorphic Strings

Difficulty: Easy
Topics: hash table, string

## Problem

Given strings `s` and `t`, return whether they are isomorphic. Characters may be
replaced to get from `s` to `t`, but the replacement must be consistent and no
two characters may map to the same character (a one-to-one mapping).

## Approach

Walk both strings together keeping two maps: `s -> t` and `t -> s`. A conflict in
either direction breaks the bijection and the answer is false.

## Complexity

Time O(n), space O(1) (alphabet bounded).

## Files

- `python/solution.py`
- `python/solution_alt.py`
