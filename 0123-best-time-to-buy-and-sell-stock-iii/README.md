# 123. Best Time to Buy and Sell Stock III

Difficulty: Hard
Topics  : dp

## Problem

At most two transactions, no overlap. Maximize profit.

## Approach

Track buy1, sell1, buy2, sell2 in one pass. Each updates from the previous pair.

## Complexity

Time O(N), space O(1).

## Files

- `python/solution.py`
