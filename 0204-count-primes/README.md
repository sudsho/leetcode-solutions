# 204. Count Primes

Difficulty: Medium
Topics  : math, sieve, number theory

## Problem

Given an integer `n`, return the number of prime numbers strictly less than `n`.

## Approach

Classic Sieve of Eratosthenes. Start assuming every number is prime, then repeatedly take the next number still marked prime and cross out all of its multiples.

Two small optimisations keep it fast: only sieve `i` up to `sqrt(n)` (any composite below `n` must have a factor at or below its square root), and start crossing out at `i*i` rather than `2*i`, because every smaller multiple of `i` already got struck by a smaller prime.

## Complexity

Time O(n log log n), space O(n) for the boolean sieve.

## Files

- `python/solution.py`
