# 121. Best Time to Buy and Sell Stock

Difficulty: Easy
Topics: array, dynamic programming

## Problem

Given prices[i] = price of a stock on day i, find the max profit from one buy and one later sell. If no profit is possible, return 0.

## Approach

Track the minimum price seen so far. At each day, profit = today minus min so far. Update best profit.

<!-- updated -->
## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
- `python/solution_alt.py`
