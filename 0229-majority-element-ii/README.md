# 229. Majority Element II

Difficulty: Medium
Topics  : Boyer-Moore voting

## Problem

Given an integer array of size n, find all elements that appear more than
floor(n/3) times. Must run in linear time and O(1) extra space.

## Approach

Generalize the Boyer-Moore majority vote: at most two values can exceed n/3,
so track two candidates with two counters. A non-matching element cancels one
vote from each. A final verification pass confirms the survivors actually clear
the threshold.

## Files

- `python/solution.py`
