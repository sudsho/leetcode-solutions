# 803. Bricks Falling When Hit

Difficulty: Hard
Topics  : union find

## Problem

Reverse the hits and use union-find to count bricks restored when each is added back.

## Approach

Union components attached to top row. Count diff after each reverse-add.

## Complexity

Time O(MN + K * inv-Ackermann), space O(MN).

## Files

- `python/solution.py`
