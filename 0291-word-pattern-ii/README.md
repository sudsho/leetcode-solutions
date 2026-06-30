# 291. Word Pattern Ii

Difficulty: Hard
Topics  : backtracking + hash map

## Problem

Given a `pattern` and a string `s`, decide whether there is a bijection between pattern characters and non-empty substrings such that substituting each character with its substring yields exactly `s`.

## Approach

Backtracking. Bound characters must match the next slice of `s`; an unbound character tries every prefix of the remaining string as its binding. A `used_words` set keeps the mapping injective, and every trial is undone before the next.

## Complexity

Exponential in the worst case (every split of `s`), but pruned hard by the prefix/used-word checks.

## Files

- `python/solution.py`
