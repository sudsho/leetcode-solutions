# 1094. Car Pooling

Difficulty: Medium
Topics  : array, prefix sum, sorting, heap

## Problem

A car drives east with a fixed `capacity` and cannot turn around. Each trip `[passengers, start, end]` picks up `passengers` at location `start` and drops them at `end`. Return whether every trip can be made without ever exceeding capacity.

## Approach

Third read of the same difference array, and the interesting part is what the accumulated value means each time. In 1109 it was the answer itself. In 2848 it was a predicate — only `> 0` mattered. Here it is a live quantity constrained at every point, so the capacity check has to sit *inside* the accumulation loop and return early on the first violation. Checking after the loop would only catch the final occupancy, which is always zero.

The off-by-one flips here and it is the whole trap. Passengers get off *at* `end`, so the cancelling `-passengers` goes at `end` and not `end + 1` — the range is effectively half-open. The habit built on the previous two problems, where the closing write always landed one past the last covered index, is actively wrong on this one. Which offset you use is a statement about the problem's semantics, not a property of the technique.

That same detail hands you the "passengers exit before others board" rule for free. A drop-off and a pickup at the same location both write into the same slot, so they net out before the running total is ever compared against capacity.

The heap alt is the version that survives unbounded locations. Sort by pickup, evict every trip whose drop-off is at or before the current stop, then board. `<=` on the eviction, for the same exit-before-boarding reason. Underneath it is doing what the array does — tracking which range updates are still open — just keyed by trip count rather than route length.

## Complexity

Difference array: time O(n + M), space O(M) for route bound M = 1000. Heap: time O(n log n), space O(n). With `end <= 1000` fixed the array is effectively O(n), and it stops being the right call the moment that bound is lifted.

## Files

- `python/solution.py`
