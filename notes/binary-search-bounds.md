# binary search bounds

six days on binary-search-on-the-answer (2528, 1552, 2064, 719, 1482, 774) and this
file still had nothing in it about binary search. writing down what the run actually
produced, since the per-problem readmes each have a piece of it and nobody rereads
those.

## the shape

two things and no more: a monotone predicate, and a bisect that finds its boundary.
everything else is whatever answering the predicate happens to take. it took a
greedy with a real exchange argument twice (2528, 1552) and a one-line ceiling sum
three times (2064, 1482, 774), and for two days i filed the exchange argument under
"part of the technique". it isn't. the variation lives in the predicate.

## which half keeps mid

- `mid = (low + high) // 2`, `high = mid` on true.
- `mid = (low + high + 1) // 2`, `low = mid` on true.

not about minimizing vs maximizing. the half that *keeps* mid is the one that has to
shrink, so the rounding goes toward the other end. got this backwards once by
reaching for "yesterday was a max so today is a min".

## bounds

read them off the structure, not "big enough to be safe". four days running that
removed a case instead of adding one - the top of the range came out feasible by
construction and no guard was needed.

then 1482, where it isn't. `m*k > n` makes the predicate constant false and a bisect
looking for a boundary that isn't there still returns something. so:

**"the range is nonempty" and "an answer exists" are different claims.** four days of
getting the second free from the first without noticing i was taking it.

and the failure mode is the thing. every bounds mistake before that one announced
itself - empty range, index off the end, an assert. a missing feasibility guard just
hands back `high`, in range and plausible and wrong. the brute force in the tests has
to be a form with no bounds at all or it agrees with the bug.

## attainment

separate question from the bisect landing somewhere. 719 searches every integer in
`[0, max-min]` and most of them are not distances between any two elements, so the
boundary could in principle land on a value nothing realizes. it can't, because
minimal `x` with `c(x) >= k` forces `c(x-1) < k`, so `c` jumped at `x`, so some pair
sits exactly there. the range being strictly bigger than the answer set is repaired
by the predicate, not by the range.

1482 avoids the question instead: the predicate is piecewise constant between
distinct bloom days, so bisecting the sorted distinct values makes the answer an
input element by construction. nicer, and less general - it needs the pieces known in
advance.

774 is where that stopped generalizing. the answer set is `d_i / j` for `j <= k+1`,
which is finite and attained and has two billion elements. **attained and enumerable
are not the same property.**

## monotonicity

check it. bisection returns something confident whether or not the predicate is
actually monotone, and twice the proof of monotonicity was more work than the
bisection.

also: there is often more than one monotonicity claim in the room and they are
unrelated. 719 has `c` non-decreasing in the limit (what the bisect uses) and `left`
never moving backwards as `right` advances (what makes the counting pass linear).
different variables, neither implies the other, and i had them fused for three days
because they share a word.

## real-valued answers (774)

- termination stops being free. `low = mid + 1` on integers strictly shrinks the
  range, so the loop halting was a proof. on floats `mid` can round to `low` and
  `low = mid` spins. fixed iteration count, not an eps - 100 halvings saturates a
  double from any starting width.
- what comes back is a bracket, not a member of the search space. correctness is a
  tolerance claim.
- **the predicate is allowed to be wrong on a measure-zero set.** the usual
  `floor(d/x)` count differs from `ceil(d/x)-1` exactly at the divisors, so it calls
  the answer itself infeasible, and the feasible set goes from `[ans, inf)` to
  `(ans, inf)`. same infimum, and the infimum is all the bisect ever reports. on the
  integer lattice that same substitution is a wrong answer, because there the
  boundary is a point of the search space. whether points have weight is the whole
  difference between the two settings.

## spare resource

2528's unspent budget, 2064's unused stores, 774's inert station. all the same
thing: the objective reads a max, and a max cannot see anything that is not the
argmax. so the witness is never canonical and the tests check the property. slack is
the generic reason for that; 1552's symmetry and 719's multiplicity are the special
ones, and i had been reading the special ones as the pattern.

## unfiled

scraps that were in here under the wrong heading, kept until they land somewhere:

- track entry seen in trie alongside word counts.
- DSU rank by component size; path compression on find.
- early return when source == target. cheap, easy to forget.
- bisect_left vs bisect_right matters when there are dups.
- another way to think about kth smallest with two heaps.
- two pointers for "at most k distinct" then subtract.
