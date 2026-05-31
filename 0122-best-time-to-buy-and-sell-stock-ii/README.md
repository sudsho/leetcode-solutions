# 122. Best Time to Buy and Sell Stock II

Difficulty: Easy
Topics: array, greedy

## Problem

You can buy and sell a stock as many times as you want (no holding more than one share). Return the maximum total profit.

## Approach

Greedy. Sum every positive day-over-day delta. That's equivalent to buying at every local minimum and selling at every local maximum, but you don't need to identify those points explicitly.

## Complexity

Time O(n), space O(1).

## Files

- `python/solution.py`
