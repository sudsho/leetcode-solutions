# 263. Ugly Number

Difficulty: Easy
Topics: math

## Problem

An ugly number is a positive integer whose only prime factors are 2, 3, and 5.
Given an integer `n`, return `true` if `n` is ugly.

## Approach

Reject non-positive `n` up front. Then repeatedly divide out all factors of 2,
3, and 5. If the leftover is 1 the number was built only from those primes;
otherwise a different prime factor remains and it is not ugly.

## Complexity

Time O(log n) - each division shrinks `n` by at least a factor of 2, space O(1).

## Files

- `python/solution.py`
