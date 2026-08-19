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

## what is being searched

1898, two days after the above was written, and the above is right about a family
narrower than i thought it was. all six problems searched a *quantity* - a budget, a
separation, a load, a bloom day, a gap width - and the monotonicity came out of the
objective, because more of the resource did more work. i had "ordered space of
candidate answers, predicate ordered along it" and never noticed that the ordered
space being the answer's own numeric value was an assumption rather than the
definition.

1898 bisects an index into an unsorted array. `removable[3]` is not bigger than
`removable[1]` in any sense the problem cares about. what `k` indexes is the set
`removable[:k]`, those sets nest by construction, and "p is still a subsequence
after deleting a set" is antitone in the set. so the predicate is monotone in `k`
because prefixes nest, and that is the whole argument - no objective, no exchange,
nothing about what a removal costs.

**what the technique needs is a chain and a predicate constant on each end of it.**
a chain of sets is a chain. the six days of numbers were a special case where the
chain happened to be an interval of integers.

worth keeping separate from "the variation lives in the predicate", which still
holds. two things vary independently: what the chain is, and what answering the
predicate takes.

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

1898 gets it free and the reason is the section above. when the chain *is* the answer
set - `k` indexes `{0..n}` and the answer is one of those indices - there is no gap
between the search space and the answer set for attainment to live in. all three of
the hard cases above are cases where the chain was a convenient superset of the
answers. so this is a question about the choice of chain and not about the problem.

2616 is the first one where both properties hold together and neither is free. an
exchange argument says an optimal pairing can be taken to use pairs adjacent in
sorted order, so the answer is one of the `n-1` adjacent gaps: attained because it is
a member, enumerable because there are `n-1` of them. the interval `[0, max-min]` is a
superset of the answer set exactly the way 719's was, and here the superset gets
*replaced* rather than repaired - the candidate-space bisect runs over the gap list
directly.

so the shape of this section is now: the search space is generically bigger than the
answer set, and there are three things to do about it. repair it at the boundary
(719, the jump in the count). replace it with the answer set (1482 by luck, 2616 by
argument). or leave it alone because the answer set is finite and still hopeless
(774). the property that decides which is available is the *size* of the answer set,
which is why 774's note had to separate attained from enumerable before any of this
could be said.

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

**that last sentence is backwards and 1898 is what showed it.** 1898's witness set
has slack in the ordinary way - "ab" embeds into "aab" two ways - and the witness is
canonical anyway, because the embeddings are ordered coordinatewise and there is a
least one. leftmost names a member and the greedy already computes it.

so slack is not what removes the canonical choice. the question is not whether the
witness set has more than one element, which it nearly always does, but whether it
has a *distinguished* element, and slack alone does not decide that. what decides it
is symmetry: 2528's budget split among tied cities has no canonical split because
permuting the cities is a symmetry of the whole problem and there is nothing left to
break the tie with. positions in a string are not symmetric, so "leftmost" is a real
choice rather than an arbitrary one.

the six days of slack cases were all symmetric too, which is why slack looked like
the generic reason. it was a confound. and the test changes with it - equality
against the canonical witness where one exists, property check where it doesn't.

**2616 says even that is not a property of the problem.** the witness is `p` disjoint
pairs. named as pairs of sorted positions it is canonical, leftmost, 1898's argument
verbatim. named as pairs of original indices it isn't, because ties in `nums` are
interchangeable and the sort picked between them by input order.

same problem, same witness set, two answers. so canonicity is relative to the space
the witness is written down in, and sorting is the step that manufactures it: a total
order laid over a multiset that only had a partial one. symmetry is still what
removes the distinguished element - what i had wrong is *where to look for it*. i was
checking the problem when the question is whether the representation has already
quotiented the symmetry away. 2528's tied cities are not more symmetric than 2616's
duplicate values; the difference is that i was still standing in the unquotiented
space when i asked.

which makes the last thirteen entries suspect as a group rather than individually.
each of them recorded a representation, not a problem, and i can't currently tell
which calls would flip under a different one. re-read them.

and the test splits rather than choosing: equality against the canonical witness in
the space that has one, property check on whatever survives the quotient.

## unfiled

scraps that were in here under the wrong heading, kept until they land somewhere:

- track entry seen in trie alongside word counts.
- DSU rank by component size; path compression on find.
- early return when source == target. cheap, easy to forget.
- bisect_left vs bisect_right matters when there are dups.
- another way to think about kth smallest with two heaps.
- two pointers for "at most k distinct" then subtract.
