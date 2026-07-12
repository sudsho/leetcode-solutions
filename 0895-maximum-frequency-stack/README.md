# 895. Maximum Frequency Stack

Difficulty: Hard
Topics  : hash table, stack, design, ordered set

## Problem

Design a stack-like structure. `push(val)` adds a value. `pop()` removes and returns the most frequent value; if several values tie for most frequent, remove the one that was pushed most recently.

## Approach

Keep two maps. `freq` tracks how many copies of each value are currently in the structure. `groups` maps a frequency `f` to a stack of the values that have reached count `f`. Track `maxfreq`, the largest frequency any value currently holds.

On push, bump the value's frequency to `f` and append it to `groups[f]`. Because the same value climbs into a higher group each time it is pushed, every group naturally holds its members in push order. On pop, take the top of `groups[maxfreq]` — that value is both the most frequent and, among the ties, the most recent, so both rules are satisfied at once. Decrement its frequency and drop `maxfreq` when that group empties.

## Complexity

Time O(1) per push and pop, space O(n) for the values held.

## Files

- `python/solution.py`
- `python/solution_alt.py` — max-heap on (frequency, insertion order), O(log n) per op
