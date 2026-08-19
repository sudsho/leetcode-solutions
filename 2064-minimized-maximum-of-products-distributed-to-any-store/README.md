# 2064. Minimized Maximum of Products Distributed to Any Store

Difficulty: Medium
Topics  : array, binary search, greedy, heap

## Problem

There are `n` specialty stores and `m` product types, with `quantities[i]` units of the `i`th type. All units must be distributed, and a store can receive units of **at most one** product type (possibly none). Return the minimum possible value of the maximum number of units given to any single store.

## Approach

Third problem running on the same outer loop - bisect the answer, answer a feasibility question inside - and the first one where the shape is visible on its own. 2528 and 1552 both had a greedy left-to-right pass as the predicate, and both times the entire difficulty was arguing about which direction that greedy pushed. Two days on direction.

There is no greedy here. The predicate is a sum.

Which means the exchange argument was never part of the technique. It was per-problem work that happened to be the hard part twice in a row, and being hard twice had quietly filed it under "binary search on the answer" as though it came with the shape. It doesn't. The shape is a monotone predicate and a bisect that finds its boundary; everything else is whatever it takes to answer the predicate, and today that is one line of arithmetic.

The collapse is bought by the store rule. A store carries at most one product type, so products never compete for the same store and the cost is additive across them. That is the real gift in the statement and it reads like a restriction. If stores could mix, the predicate would be a bin-packing question and none of this survives.

Given additivity, fix product `i` and ask how well `k` stores can carry it. Spreading `q` units over `k` stores leaves the fullest holding at least `ceil(q/k)` by pigeonhole, and an even split achieves exactly that - so the best possible maximum for one product on `k` stores *is* `ceil(q/k)`. Inverting, `ceil(q/k) <= x` iff `q <= k*x` iff `k >= ceil(q/x)`. Holding product `i` under `x` costs exactly `ceil(q_i/x)` stores, no fewer, and no search finds it. Sum over `i`, compare against `n`.

Monotonicity is the only thing the bisect actually leans on, and here it needs no argument: `ceil(q/x)` is non-increasing in `x`, so the total is, so the predicate is upward closed. Every earlier version of this predicate needed an exchange claim before it could be called monotone.

The bisection form flips from yesterday - `mid = (low + high) // 2` with `high = mid` on success, where 1552 needed `(low + high + 1) // 2` with `low = mid`. That off-by-one is a property of which side absorbs `mid`, not of the problem: the half that keeps `mid` has to be the one that shrinks, so rounding goes toward the other end. Worth writing down, since it looked for two days like something to memorize per problem.

The upper bound `max(quantities)` is always feasible - the sum becomes `m` ones and `m <= n` is promised - so the range is nonempty and the answer exists without a guard. Second day running that the bound removes a case rather than adding one, both times because it was derived from the structure instead of picked large enough to be safe. Unused stores stay unused for the same reason 2528 left budget unspent: an extra store lifts nothing, and the objective only reads the fullest one.

The distribution alternate is the ninth day of the summary-versus-set split and the third straight non-canonical witness, but for a new reason. 1552's ambiguity was a symmetry - the mirror gave a different placement with no way to prefer an end. Here it is slack: the counts only need to sum to at most `n`, so a leftover store can go to a product that is not the bottleneck, dropping its load without moving the maximum. So the counts returned are the minimal ones, not the only ones, and the tests replay them rather than compare them across callers.

The heap alternate hands out the `n - m` spare stores one at a time, always to whichever product currently has the worst even-split load. It is kept because it is a genuinely different algorithm - no predicate, no ceiling-sum, no monotonicity claim - and the last two days both ended with two callers sharing an inner loop, which made their agreement weaker evidence than it looked.

## Complexity

Primary: `O(m log W)` time, `O(1)` space, where `W = max(quantities)`. Heap: `O(m + (n - m) log m)`, worse whenever the store count dwarfs the product count, which is the usual case. Distribution: primary plus `O(m)` for the witness. Saturated: `O(m)`.

## Files

- `python/solution.py`
