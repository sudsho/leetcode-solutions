# 2226. Maximum Candies Allocated to K Children

Difficulty: Medium
Topics  : binary search, greedy, math

## Problem

Given `candies`, where `candies[i]` is the size of pile `i`, and an integer `k`. A pile may be divided into any number of sub-piles of equal size, and piles may not be merged. Give `k` children the same number of candies each and maximize that number. Return `0` if it cannot be done.

## Approach

Twelfth on the monotone-predicate-plus-bisect shape. Fix a size `t`; pile `c` yields `c // t` whole sub-piles and the remainder is stranded, so feasibility is `sum(c // t) >= k`. Bisect on `t` over `[1, total // k]`.

The predicate is `O(n)` with no allocation, and its monotonicity is the plainest in the run - `c // t` is non-increasing in `t`, a sum of non-increasing functions is non-increasing, so the feasible set is a prefix. No greedy to read it off, no concavity, no lattice.

Eleven days of monotonicity being the thing that needed the argument had me reading it as where the content lives. It isn't. It is the admission ticket, and today everything interesting is somewhere else.

## The axis from yesterday was one notch too coarse

Yesterday's claim was that the ten problems before 1802 all bisected because their predicates were black boxes - objects you could only *call* - and that 1802 was different because its predicate was an expression, so it could be inverted rather than searched. I wrote that the separating axis is black box versus expression, and that unlike the 21st's finding this one is a property of the problem rather than of the constraint block.

This predicate is an expression. `sum(c // t) >= k`, written down, nothing simulated, no greedy inside it. And it is not invertible, and no amount of staring makes it invertible.

The reason is that `sum(c // t)` is a step function with a breakpoint at every value of `c_i // q`, and there are `O(n sqrt(C))` of those. 1802's predicate had **three** pieces, with breakpoints at `min(left, right)` and `max(left, right)`, each piece a solvable one-variable inequality. That is what made inverting it possible - not that it was writable, but that its pieces were few and locatable.

So the axis is not black box versus expression. It is how many pieces the predicate has, and whether you can find them without looking at all of them. Which is a size question, and I had thought I was replacing the size question with something better.

What survives is that the size in question changed. On the 21st the comparison was `log(range)` against `|answer set|`. The right comparison is `log(range)` against the number of *breakpoints you can locate cheaply*, and 1802 wins that one at three while today's loses it at several million. Same shape of comparison, different quantity, and the new quantity is at least about the predicate rather than about the answer.

## Attainment, and the first answer set bigger than the input

**The answer is always `c // q` for some pile `c` and some positive `q`.** Let `t` be the answer, so `t` is feasible and `t + 1` is not. Something must break between them, so some pile has `c // t > c // (t + 1)`. Put `q = c // t`. Then `q * t <= c` and `c < q * (t + 1)`, so `t <= c / q < t + 1`, so `c // q = t`.

Two inequalities and a division. The previous attainment proofs all went through an exchange argument on a greedy, and this is the first one that is just arithmetic.

The answer set is the distinct values of `c // q`, which is `O(sqrt(c))` per pile and `O(n sqrt(C))` overall. At the constraint ceiling - `n` up to `1e5`, `C` up to `1e7` - that is several million against 24 predicate calls.

**And it is the first time the answer set has not been `n` on the nose.** The previous eleven were one candidate per input element: a gap, a ratio, a threshold value. This one is a divisor lattice, so the candidates are indexed by pairs and the count is superlinear. On the 21st I concluded the comparison was decided by the venue, because `|answer set| >= n` always while `log(range)` is capped by the width of a machine integer. Three days later the answer set has got bigger for a structural reason unlike any of the eleven. It has never once got smaller.

## Two witnesses, and only one of them is canonical

Eighteenth day of the summary-versus-set split, and the first time the two witnesses in the room disagree.

There are two objects here, and eleven days of them coinciding had me treating them as one:

- the **certificate**, which proves `t` feasible: a vector `v` with `v_i <= c_i // t` and `sum(v) >= k`;
- the **allocation**, which is what the problem asks for: exactly `k` sub-piles assigned to `k` named children.

Yesterday these were the same object - the tent was simultaneously what bounded the sum and what you would hand in. On the 21st they came apart for the first time, the work count proving feasibility and the schedule needing a separate construction. Today they come apart again, and the canonicity lands on the other one.

The certificate set is closed under pointwise **maximum**: joining two certificates keeps every coordinate under its own bound and only raises the sum. A nonempty set of integer vectors closed under join and bounded above has a **greatest** element, and it is `v_i = c_i // t` - take everything.

So the certificate is canonical by yesterday's argument run upside down, and that the dual works is not a coincidence of the two problems. Yesterday's constraint was an upper bound on a sum, so shrinking was safe and the meet survived. Today's is a lower bound on a sum, so growing is safe and the join survives. **The direction of the lattice is set by the direction of the constraint.** I had read 1802's meet-closure as a fact about that problem's geometry; it is a fact about which way the inequality points, and the geometry was along for the ride.

The allocation is not canonical and cannot be made so. Children are interchangeable by definition, which is 2141's `n!` relabelings verbatim, and on top of that the certificate almost always has slack - `sum(c_i // t)` overshoots `k` - so there is a choice of which sub-piles go unused before there is any question of who gets what. Two independent reasons stacked, where the 20th and 21st had one each.

The tests split accordingly: equality against the greatest element for the certificate, property check for the allocation. A property check on the certificate would pass on any smaller vector and prove nothing, which is the whole reason today is worth writing down.

## Bounds

Eighth day, and the bottom end is a kind that has not come up.

The previous eleven bottoms were either trivially feasible by arithmetic (2141's `t = 0` needs no work) or promised feasible by the statement (1802's all-ones array, 1898's empty removal set). Here the bottom of the search space is `t = 1`, and `sum(c // 1) = total`, so it is feasible exactly when `total >= k` and infeasible otherwise.

`t = 0` is not the answer to that, because it is not in the search space at all - the predicate does not extend there, since `c // 0` is not a number. So the `0` this returns is a value the problem defines *outside* the search rather than a point the search reaches, and the guard is forced by the arithmetic of the predicate rather than by a convention about what to report when nothing works.

1482 returned `-1` from a predicate that was perfectly well defined at the impossible point and merely false there. This is the first time the predicate has a domain that stops, and the difference matters: 1482's guard could have been folded into the search with a wider range, and this one cannot.

The top end `total // k` is a bound and not an achievable configuration. `[1, 1, 5]` with `k = 3` has a ceiling of `2` and an answer of `1`, because the two singleton piles cannot be merged into a second pile of size 2. Fourth day running that the ceiling is unattained, and the reason has 2141's shape - a resource that exists and cannot be delivered where it is needed.

## Complexity

Primary: `O(n log(total / k))`, with the log capped near 24 at the constraint ceiling. Candidate search: `O(n sqrt(C))` to build and `O(n log)` to search, unusable at the ceiling and kept because agreement with the primary tests the attainment proof. Certificate and allocation: `O(n)` each after the primary.

## Files

- `python/solution.py`
