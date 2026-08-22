# 1802. Maximum Value at a Given Index in a Bounded Array

Difficulty: Medium
Topics  : binary search, greedy, math

## Problem

Construct an array `nums` of length `n` of positive integers with `|nums[i] - nums[i+1]| <= 1` and `sum(nums) <= maxSum`. Return the largest possible `nums[index]`.

## Approach

Eleventh on the monotone-predicate-plus-bisect shape, and the first where the predicate is `O(1)`.

The previous ten all had a scan in them - a greedy on nine, a sum over the batteries on the tenth - so evaluating the predicate cost a pass over the input, and the only thing you could do with it was call it at a point.

Here it is a closed form. Fix the peak value `v`; the cheapest legal array with that peak is the clamped tent `max(1, v - |i - index|)`, and its sum is two arithmetic runs with a clamp. Each run is linear in `v` while it stays above the floor and quadratic once it hits it, with the breakpoint at the side's length. No loop, no allocation, no touching the input.

## The lattice, and why it gives both halves at once

Seventeenth day of the summary-versus-set split, and the first canonical witness in the run.

The two before this were non-canonical for the two different reasons the notes finally separated on the 20th and 21st - slack with no symmetry, where the leftmost rule still named a member, and symmetry that no rule could break. Today there is nothing to pick between, because there is exactly one thing to pick.

Fix `v` and let `S` be the set of legal arrays with `v` at the index. `S` has a **least element** under the pointwise order, and it is the tent. Directly: any `a` in `S` has `a[index] = v` and moves by at most one per step, so `a[i] >= v - |i - index|`; entries are positive, so `a[i] >= 1`; so `a >= max(1, v - |i - index|)` pointwise, and the tent is itself in `S`.

The reason it works is what the direct proof hides. `S` is closed under pointwise minimum - positivity survives a min, and `|min(a_i, b_i) - min(a_j, b_j)| <= max(|a_i - a_j|, |b_i - b_j|) <= 1` for adjacent positions - and a nonempty set of positive integer arrays closed under meet has a least element. So canonicity here is a lattice fact about the constraints rather than a convention for breaking a tie, which is a third thing the word can mean on top of the two the 21st separated.

**And it is why the predicate is a closed form.** Feasibility at `v` asks whether *some* legal array with that peak has sum at most `maxSum`; sum is monotone in the pointwise order, so that is whether the *least* one does. The least one is written down rather than searched for, and its sum is arithmetic. One property - meet-closure - producing the canonical witness and the `O(1)` predicate together.

Monotonicity comes from the same place, which is also new. Nine of the previous ten read it off a greedy and the tenth had to go through concavity because both sides of the inequality moved. Here `max(1, v - d)` is non-decreasing in `v`, so the least array is pointwise non-decreasing in `v`, so its sum is, so the feasible set is a prefix. Strictly increasing in fact, since the entry at the index *is* the peak - so there is no plateau and the boundary is a point rather than the top of a flat stretch.

## Bounds

Seventh day. The bottom end `v = 1` is the all-ones array with sum `n`, and the constraints promise `n <= maxSum` - feasible by a promise in the statement rather than by arithmetic, so 1898's bottom end and not 2141's.

The top end `maxSum - n + 1` comes from keeping only "every other entry costs at least 1" and throwing away the tent's shape, and a discarded constraint gives an upper bound rather than an achievable configuration. `n = 3, index = 1, maxSum = 6` has a ceiling of 4 and an answer of 2, because a peak of 4 in the middle drags both neighbours up to 3. Third day running that the top end is a bound with nothing attaining it, and by now the surprise is the nine days before, where the extreme threshold happened to be achievable every time.

## Inverting instead of searching

`_minimum_sum` as a function of the peak is piecewise polynomial with breakpoints at `min(left, right)` and `max(left, right)`: quadratic while both sides are clamped, quadratic with one side free, linear once both are free. Each piece is a one-variable inequality and every one of them can be solved. Take the root of each piece, keep the ones landing inside their own piece, return the largest that passes. `O(1)`, no search of any kind.

**This is the move the eleven days were missing, and unlike the 21st it is inside the mathematics.**

The framework says the search space is generically bigger than the answer set, and which move you get depends on the answer set's size against the cost of the search it replaces. On the 21st that comparison turned out to be settled by the constraint format - `log(range)` capped by the width of a machine integer, `|answer set|` capped by nothing - so its result was decided before I opened the first problem, by the venue rather than by the problem. I wrote that night that I did not think the rule was wrong, only that I could not test it here. That was true and it was also me not looking at the right thing.

Both branches of that comparison are searches, and a search is what you do with a predicate you can only *call*. Ten days of predicates that were scans, and the only handle any of them offered was evaluation at a point. Bisection is the general method for exactly that situation, and its cost is the price of having no other handle.

This predicate is a formula, so it has another handle. Inverting it is not a cheaper search - it is not a search. The axis separating today from the previous ten is not the size of anything; it is whether the predicate is a black box or an expression. That is a property of the problem and not of the constraint block.

It also renames the axis I proposed on the 21st. I said the question was whether membership in the answer set is decidable locally, on the strength of 2141's peel. Right observation, wrong name: the peel worked because the predicate's structure was exposed, and local decidability was one symptom of that. "Locally decidable" and "invertible" are two ways the same thing shows up.

## The floor that does not lose anything

I wrote the inversion first with a `+/- 1` window around every root, on the assumption that `isqrt` and `//` compound and cost one. They do not.

For integer `c` and real `s >= 0`, let `m = floor((c + s) / 2)`. Then `2m - c <= s` and `2m - c` is an integer, so `2m - c <= floor(s)`, so `m <= floor((c + floor(s)) / 2)`. The other direction is `floor(s) <= s`. The inner floor is free, and the same argument covers `1 + isqrt(r)` and the plain `//` in the linear piece.

The window came out and the equality is asserted against a widened search instead, so the claim is tested rather than reasoned about once and trusted. Flooring an upper bound and flooring an answer are different operations that happen to agree on this expression, which is not a general licence.

## Complexity

Primary: `O(log maxSum)` with an `O(1)` predicate, so `O(log maxSum)` total and no dependence on `n` at all. Inversion: `O(1)`. Witness: `O(n)`, the first honest linear cost in the file, and it is the witness's cost rather than the answer's. Bisect-on-witness, kept as a cross-check: `O(n log maxSum)`, which is what the previous ten cost.

## Files

- `python/solution.py`
