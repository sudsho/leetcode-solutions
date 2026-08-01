# 2381. Shifting Letters II

Difficulty: Medium
Topics  : array, string, prefix sum

## Problem

Given a lowercase string `s` and `shifts[i] = [start, end, direction]`, shift every character in `s[start..end]` forward one letter if `direction == 1` and backward one letter if `direction == 0`, wrapping at the alphabet ends. Return the string after all shifts.

## Approach

Fourth difference-array problem of the day, and the first where the range update is not obviously numeric. The move is noticing that letter shifts **compose additively**: forward 3 then back 1 is forward 2, and the order they were applied in does not matter. That is the precondition the technique actually needs. A pile of overlapping shifts over a position collapses into one net integer, so the whole shift list becomes two writes each and one accumulate at the end.

If the operation were order-dependent the array would be useless and every shift would have to be replayed in sequence — worth stating explicitly, because "range update" alone is not enough to reach for this. Commutative and additive is.

The offsets go back to `end + 1`, since these ranges are inclusive and `end` really is shifted. That is the opposite of 1094, where drop-offs at `end` made the range half-open. Two problems in a row with the closing write in different places is a good argument for reading the range semantics every time rather than trusting the last one.

The `% 26` is doing real work rather than just wrapping `z -> a`, because the net shift can reach `± len(shifts)`. Python's `%` returns a non-negative result for a positive modulus, so `-3 % 26 == 23` and backward shifts wrap for free — the same free lunch as the remainder buckets in 974, and the same thing that needs `((x % 26) + 26) % 26` in Java or C++.

## Complexity

Time O(n + m) for string length n and m shifts — two writes per shift, one pass to accumulate and rebuild. Space O(n) for the difference array plus the output. The naive per-index replay is O(n · m), which at n, m ≤ 5 · 10⁴ is the 2.5 billion updates the constraints exist to rule out.

## Files

- `python/solution.py`
