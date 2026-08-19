# 2528. Maximize the Minimum Powered City

Difficulty: Hard
Topics  : array, binary search, greedy, prefix sum, sliding window

## Problem

`stations[i]` is the number of power stations in city `i`. A station in city `j` powers every city within range `r`, so the power of city `i` is the total number of stations in `[i-r, i+r]`. Given `k` additional stations to place in any cities, return the largest possible value of the minimum power over all cities.

## Approach

2772 fixed the operation width and found the choice disappeared: the leftmost position still owing something could be served by exactly one window, induction pinned every count, and all that remained was checking whether the forced answer was legal. This problem fixes the width too - every station covers exactly `2r+1` cities - and the choice comes back.

What changed is the target. 2772 wanted the array to land on zero *exactly*, so a window serving `i` had to start at `i`; anything further left would overshoot a settled position, and overshoot was fatal because operations only subtract. Here the requirement is `power[i] >= x`, an inequality, so overshoot costs nothing. A station covering city `i` may sit anywhere in `[i-r, i+r]`, and the cities to its left that it also covers are already satisfied and cannot be harmed by more.

So the argument stops being a forcing argument and becomes an exchange. Every legal placement serving `i` covers `i`; the rightmost one also covers the longest suffix of what is still ahead; nothing behind `i` can object. Push right and no solution is lost. That is strictly weaker than what 2772 proved - there the multiset was unique, here many placements are optimal and the greedy merely names one.

The rightmost legal city is `min(i + r, n - 1)`, and the clamp is not a boundary patch but the statement that stations live in cities. It still covers `i`: if `i + r >= n` then `i > n - 1 - r`, so city `n-1` is within `r` of `i` anyway.

The outer question is a maximin, which the sweep cannot answer directly. Binary search converts it - "can every city reach `x` on a budget of `k`" is monotone in `x`, and that predicate is precisely the sweep. So the shape here is one layer taller than everything else this week: the difference array is no longer the algorithm, it is the feasibility oracle inside one.

Two failure modes vanish relative to 2772. `remaining < 0` cannot happen because the target is a lower bound rather than an equality, and the window cannot run off the end because the clamp always yields a legal placement. The only way to fail is to exhaust the budget, which is why the check is a running total against `k` and nothing else. Ninth syntax for the half-open closing index in about a week and a half, here `min(i + r, n - 1) + r + 1`.

The placement alternate returns a witness rather than *the* witness, which inverts the summary-versus-set call yet again. In 2772 the set was the honest object because it was unique and the bool sat lossily on top of it. Here the exchange argument only says rightmost is *as good as* anything, so two callers can legitimately disagree and the result cannot be validated by comparison - it has to be replayed. It also leaves the unspent budget unspent on purpose: a station built after the sweep is satisfied raises some city above the minimum and cannot raise the minimum itself, so it is invisible to the objective.

The linear scan alternate climbs candidate targets one at a time instead of bisecting. It is `O(n · answer)` and unusable on the real constraints, kept because it separates the two ideas the primary fuses. The sweep is a feasibility test and nothing more; the monotonicity of that test is a separate observation. Walking the targets in order makes that assumption something the code visibly leans on rather than something buried in a bisection that would return quiet nonsense if it failed.

## Complexity

Primary: `O(n log(S + k))` time where `S` is the total number of existing stations, `O(n)` space. Placement: same, plus `O(n)` for the counts. Linear scan: `O(n · answer)` time, `O(n)` space.

## Files

- `python/solution.py`
