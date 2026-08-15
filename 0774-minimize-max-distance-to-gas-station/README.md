# 774. Minimize Max Distance to Gas Station

Difficulty: Hard
Topics  : array, binary search, heap, greedy

## Problem

`stations` holds sorted positions on a line. Add `k` more stations anywhere, not necessarily at integer positions. The penalty is the largest distance between adjacent stations. Return the smallest achievable penalty, to within `1e-6`.

## Approach

Sixth problem on the monotone-predicate-plus-bisect shape, and the first where the answer is not an integer. I expected that to be a detail about the loop condition. It changes what the bisect is allowed to claim, and in the one direction I would not have guessed.

The setup is unchanged. Adding a station only ever shortens a gap, so the count needed to bring every gap under `x` is non-increasing in `x`, `needed(x) <= k` is upward closed, and the bisect finds its boundary. The predicate is a ceiling sum, `sum ceil(d_i / x) - 1`, with the gaps independent because a station dropped in one does nothing for any other. That puts it next to 2064 rather than next to 2528 and 1552, where the inner greedy was doing real work. Four of the six now have a trivial predicate, which keeps pointing at the same conclusion: the variation in this shape is in what the predicate *is*, not in how it gets answered.

What is new is that the search space is the reals, and three things break.

**Termination stops being free.** On the integer lattice `low = mid + 1` strictly shrinks the range every iteration, so the loop terminating was a proof rather than a hope. On floats `mid` can round to `low`, `low = mid` moves nothing, and it spins. Five days of `while low < high` without ever having to think about progress. A fixed iteration count is the fix, and it is worth being explicit that this is now a precision parameter and not something derived from the problem.

**The answer is no longer a point I can return.** The bisect returns an endpoint of a bracket and the claim is that the true answer lies inside it. Correctness became a tolerance claim rather than an equality.

**And the predicate is allowed to be wrong.** This is the day. On integers every point of the search space had weight, so a predicate that misfired at one value moved the boundary by one and that was a wrong answer. Here the boundary is a limit of the feasible set, so the predicate can be wrong on any measure-zero set without moving it. Almost every implementation of this problem counts with `floor(d / x)` instead of `ceil(d / x) - 1`. Those differ exactly when `d / x` is an integer, where floor is one larger, so the floor version calls infeasible something that is feasible, and the single point it gets wrong is the correct endpoint itself. The floor-feasible set is `(answer, inf)` where the true one is `[answer, inf)`. A set and its closure have the same infimum, and the bisect only ever reports the infimum, so the error is invisible. Both counts are in the file and the tests check that they disagree pointwise on precisely the divisors and that the two searches still land on the same limit. The same substitution on any of the previous five days would have been fatal. What decides which it is: whether points have weight.

The exact alternate is a greedy rather than a search. The penalty for an allocation is `max_i d_i / (c_i + 1)`, and handing the next station to whichever gap currently has the largest `d_i / (c_i + 1)` is optimal by exchange, since that gap attains the current maximum and nothing placed elsewhere lowers it. Run on a heap with `Fraction` keys it produces the answer exactly. It is kept because it shares nothing with the bisect: no predicate, no monotonicity claim, no bounds, no floating point. Several days in this run kept alternates that shared their inner loop with the primary, and I had been counting that agreement as a cross-check when it mostly was not one. This one is slower where it counts, linear in `k` against the bisect's hundred passes over the gaps, which is why the bisect stays primary.

Yesterday ended on 1482's candidate set being the input itself, small enough to bisect over directly, which made the attainment question disappear instead of answering it. The same set exists here: the answer is `d_i / j` for some gap and some `j <= k + 1`. It just has `|gaps| * (k + 1)` elements, two billion at the constraint ceiling. So it works as a brute force on small inputs and as nothing else. The answer being attained does not make it enumerable, and I had been treating those as the same fact.

Twelfth day of the summary-versus-set split, fourth straight non-canonical witness. Yesterday closed on slack being the generic case with symmetry and multiplicity as the special ones, and this is the first test of that. It is slack, in the most literal form yet: stations that change nothing at all. Two gaps of 10 with `k = 1` give a penalty of 10 whichever gap the station lands in, because the untouched gap sets the maximum either way. The station is not reallocatable so much as inert. Same shape as 2528's unspent budget and 2064's unused stores, three problems now with a resource the objective cannot see, always because the objective reads a max and a max ignores everything that is not the argmax.

## Complexity

Primary: `O(n log(W / eps))` time, fixed at 100 iterations, `O(n)` space for the gaps. Exact greedy: `O((n + k) log n)` with exact rational arithmetic on top. Single-gap shortcut: `O(1)`.

## Files

- `python/solution.py`
