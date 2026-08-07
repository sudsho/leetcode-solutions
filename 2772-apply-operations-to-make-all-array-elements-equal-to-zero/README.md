# 2772. Apply Operations to Make All Array Elements Equal to Zero

Difficulty: Medium
Topics  : array, prefix sum

## Problem

Given `nums` and an integer `k`. One operation picks any subarray of size exactly `k` and decreases every element of it by `1`. Return `true` if the array can be made all zeros, `false` otherwise.

## Approach

1526 ran the difference-array map backwards: given the array, find the cheapest multiset of range updates producing it. This runs it backwards as well, with a single freedom removed — every operation is exactly `k` wide. Removing that one freedom changes what kind of question it is, which is the thing worth keeping.

In 1526 an operation could be any width, so many multisets produced the target and the question was which is smallest. Here there is at most one. Index `0` can only be touched by an operation starting at `0`, so the count starting there is pinned to `nums[0]`. That fixes index `1`'s remaining demand, and only an operation starting at `1` can still reach it, so that count is pinned too. Induction runs the length of the array.

So there is nothing to minimize. The operation multiset is a function of the input rather than a choice, and the only remaining question is whether the single candidate is legal — which is why the problem returns a bool instead of a count. Calling the sweep greedy is a slight lie: greedy implies choosing well at each step, and here there is never a second option to pass over.

The forced-choice argument is the same one as 995, where a bit still reading `0` at `i` could only be fixed by opening a window at `i`. The difference is in what gets tracked, not in the argument. Flips compose mod 2, so 995 carried a parity; decrements compose over the integers, so this carries a running count. The shape survives the change and the state does not.

Two ways the forced multiset turns out to be illegal:

- `remaining < 0` — operations already in flight have driven this position below zero, and nothing recovers it since every operation only subtracts.
- `i + k > n` — the position still owes something and no `k`-wide window covering it fits inside the array.

The difference array here holds operations rather than values: one opened at `i` covers `[i, i+k-1]` and stops counting at `i+k`. That closing index is the half-open form, and the notable thing is that it is *pinned* rather than chosen. In 1526 the closes were free precisely because a close could be paired against any already-open start; here it lands `k` steps after its open and nowhere else, so it can run off the end and make the instance infeasible. Eighth syntax for that boundary in about a week, and the first time the boundary is a source of failure rather than an off-by-one to get right.

The reconstruction alternate returns the operations instead of the bool, which makes the determinism visible rather than argued — what comes back is not *a* solution but *the* solution. That inverts the summary-versus-set call that has picked the alternate on each of the previous five days. There the summary sufficed and the set was kept against a hypothetical follow-up; here the set is what the computation actually produces, and the bool is the lossy thing.

The `O(n·k)` version subtracting across a working copy is too slow on the real constraints but states the forced recurrence with nothing in front of it. The primary's counter is exactly that inner subtraction deferred — both compute the same `remaining` at every index, one having already paid and one paying when the value is read. It also makes the tail condition obvious: the loop stops at `n - k`, so the last `k - 1` positions never get an operation of their own and must reach zero as a side effect of earlier windows. `i + k > n` is that same fact stated one index at a time.

## Complexity

Primary: `O(n)` time, `O(n)` space for the expiry array. Reconstruction: same, plus `O(n)` for the operation counts. Direct subtraction: `O(n·k)` time, `O(n)` space.

## Files

- `python/solution.py`
