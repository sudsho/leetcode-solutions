# 1482. Minimum Number of Days to Make m Bouquets

Difficulty: Medium
Topics  : array, binary search

## Problem

`bloomDay[i]` is the day the `i`th flower opens. A bouquet needs `k` **adjacent** flowers, all open. Return the earliest day on which `m` bouquets can be cut, or `-1` if it can never be done.

## Approach

Fifth problem on the monotone-predicate-plus-bisect shape. The last four days all ended on some version of *the bounds came off the structure and needed no guard*, and by day four I had started reading that as a property of the technique. It is not. Today it breaks, and the way it breaks is the day.

Waiting only ever opens flowers. It never closes one and never adds one. So the number of bouquets available on day `d` is non-decreasing in `d`, the predicate `bouquets(d) >= m` is upward closed, and the bisect applies exactly as before.

What is different is that the predicate can be **false everywhere**. `m` bouquets of `k` adjacent flowers consume `m * k` flowers, and if the garden holds fewer than that, no day is feasible. A monotone predicate that never turns on has no boundary, and a bisect looking for one will still return something.

Every earlier problem in this run was feasible at the top of its range by construction - 2528 could always power every city given budget, 1552 could always separate two balls, 2064 degenerated to one product per store, 719's multiset certainly contained a `k`th element. So "the search range is nonempty" and "an answer exists" were the same statement, and I had been collecting the second for free from the first without noticing.

The reason this is worth the day rather than a line is that the failure is **silent**. Skip the guard and `low` converges to `high = max(bloomDay)`, which is in range, plausible, and wrong. Every previous bounds mistake in this run announced itself - an empty range, an index off the end, an assertion. This one just returns a number.

Past the guard the range is tight at both ends, and the guard is what makes the top end correct rather than being a case bolted on beside it. `min(bloomDay)` is the first day anything is open at all. `max(bloomDay)` is the day the whole garden is open, and that is feasible *precisely because* `m * k <= n` was already established.

The greedy inside the predicate needs the shortest argument of the run so far. Inside a maximal run of `L` open flowers the count is `L // k` regardless of placement, since bouquets consume `k` each and cannot overlap - so there is nothing to choose and cutting as early as possible is optimal by default. That puts this closer to 2064's ceiling sum, a formula wearing a loop, than to 2528 and 1552 where the inner greedy was doing real work and the exchange argument was most of the difficulty.

Yesterday ended on the search range being strictly larger than the set of possible answers, repaired after the fact by the boundary being a jump in the count. Here the two sets can be made to coincide: the bloomed set only changes on days something blooms, so the predicate is piecewise constant between consecutive distinct values of `bloomDay` and the answer is always one of them. The value-space alternate bisects those directly, which makes the attainment question disappear rather than answering it. It stays an alternate because the integer bisect is the part that generalizes - it needs only monotonicity, where this needs the pieces known in advance, which is a property of this problem and not of the shape.

Eleventh day of the summary-versus-set split, and the first **repeated** reason for a non-canonical witness. 1552's was symmetry, 2064's slack, 719's multiplicity; this one is slack again, since a run with `L % k != 0` has spare flowers and the bouquets slide within it. The repeat is the point. Three distinct reasons in a row had me half-expecting a new one each time, as though they were a list being enumerated. Slack is the generic case - whenever the objective reads a threshold instead of the whole assignment, the leftovers are free - and symmetry and multiplicity were the special ones.

## Complexity

Primary: `O(n log W)` time where `W = max(bloomDay) - min(bloomDay)`, `O(1)` space. Value-space: `O(n log n)` for the sort then `O(n log n)` for the search. Witness: primary plus one pass. Single-flower: `O(n log n)` for the sort alone.

## Files

- `python/solution.py`
