# 38. Count And Say

Difficulty: Medium
Topics  : string, simulation

## Problem

The count-and-say sequence is defined recursively: start with "1", and each next term describes the previous one by reading off groups of consecutive equal digits as "count digit". So "1" -> "11" (one 1), "11" -> "21" (two 1s), "21" -> "1211", and so on. Given n, return the nth term.

## Approach

Straight simulation. Keep the current string, and at each step walk it left to right, expanding runs of the same character into "count + char". Repeat n-1 times.

## Complexity

Each term can roughly double in length, so time is O(2^n) in the worst case which is fine for the given constraints. Space is O(length of current term).

## Files

- `python/solution.py`
