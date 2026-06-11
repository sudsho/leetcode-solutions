# 338. Counting Bits

Difficulty: Easy
Topics: dynamic programming, bit manipulation

## Problem

Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), ans[i] is the number of 1 bits in the binary representation of i.

## Approach

Right-shifting i by one drops its lowest bit, leaving a smaller value we have already computed. The dropped bit is just i & 1. That gives the recurrence ans[i] = ans[i >> 1] + (i & 1), so the whole table fills in a single pass.

## Complexity

Time O(n), space O(n) for the output.

## Files

- `python/solution.py`
