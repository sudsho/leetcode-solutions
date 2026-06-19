# 93. Restore IP Addresses

Difficulty: Medium
Topics: string, backtracking

## Problem

A valid IP address consists of exactly four integers (each between 0 and 255, no leading zeros) separated by single dots. Given a string of digits, return all possible valid IP addresses formable by inserting dots into it, in any order.

## Approach

Backtracking that places exactly four segments of 1-3 digits each. A segment is valid when it has no leading zero (unless it is "0") and is at most 255. Two prunes keep it cheap: stop as soon as the remaining characters can't fill the segments still owed, and break out of the size loop once a segment would run past the end.

## Complexity

Constant-bounded search (at most 3^4 splits), so effectively O(1) for the fixed four-segment structure; O(n) to slice and join.

## Files

- `python/solution.py`
