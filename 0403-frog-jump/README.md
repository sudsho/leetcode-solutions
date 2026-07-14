# 403. Frog Jump

Difficulty: Hard
Topics: dynamic programming, hash table

## Problem

A frog crosses a river by hopping on stones at the given sorted positions. It starts on the first stone and the first jump must be 1 unit. If its last jump was `k` units, the next may be `k-1`, `k`, or `k+1` units (positive). It can only land on a stone. Return whether it can reach the last stone.

## Approach

DP over states `(stone, last jump size)`. Keep `reachable[pos]` = the set of jump sizes that can land the frog on `pos`. Seed `reachable[1] = {1}`, then sweep stones left to right, expanding each recorded jump into `k-1, k, k+1` and recording any that land on a real stone. If a jump lands on the last stone, we're done.

## Complexity

Time O(n^2) states, space O(n^2) in the worst case.

## Files

- `python/solution.py`
