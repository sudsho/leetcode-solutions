# 850. Rectangle Area II

Difficulty: Hard
Topics  : sweep line, segment tree

## Problem

Total area covered by axis-aligned rectangles, modulo 1e9+7.

## Approach

Coordinate compress on x. For each y-event, mark interval add or remove. Sum coverage between y-events.

## Complexity

Time O(N^2) with simple sweep; segment tree gives N log N.

## Files

- `python/solution.py`
