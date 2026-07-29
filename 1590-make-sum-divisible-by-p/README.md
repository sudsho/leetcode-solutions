# 1590. Make Sum Divisible by P

Difficulty: Medium
Topics  : array, hash table, prefix sum

## Problem

Given an array `nums` and an integer `p`, remove the smallest possible non-empty contiguous subarray so that the sum of the remaining elements is divisible by `p`. Return the length of that subarray, or `-1` if it cannot be done. Removing the entire array is not allowed.

## Approach

Restate the goal in terms of what gets removed rather than what is left. Let `target = total % p` — that is the excess the removed slice has to carry. If it is already zero the answer is 0 and nothing is deleted. Otherwise we want the shortest slice whose own sum is congruent to `target` mod `p`.

That is a prefix-sum lookup again, but with a shift. The condition `prefix[i] - prefix[j] ≡ target (mod p)` rearranges to `prefix[j] ≡ prefix[i] - target (mod p)`, so at each right end there is exactly one earlier remainder worth searching for. 974 is the special case where the wanted difference is 0 and you look up the current remainder; here the lookup is displaced by the debt.

The map direction flips too, and this is the part that took a second pass. 523 and 525 store the *first* index for each remainder because they want the longest window. This problem wants the *shortest*, so the stored index is overwritten every time — a later index with the same remainder beats an earlier one for every future right end, so there is no reason to keep the older one around. Same map, opposite update rule, driven entirely by whether the objective is a max or a min.

Two guards matter. `(running - target) % p` has to go through the modulus so a negative intermediate wraps back into range. And a best length equal to `n` means the only slice that works is the whole array, which the problem forbids, so that case returns `-1` even though the arithmetic succeeded. Seeding the map with `{0: -1}` is what allows a prefix-length slice to be a candidate at all.

## Complexity

Time O(n) for the single pass, space O(min(n, p)) for the remainder map.

## Files

- `python/solution.py`
