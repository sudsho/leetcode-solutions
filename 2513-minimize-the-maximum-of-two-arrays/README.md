# 2513. Minimize the Maximum of Two Arrays

Difficulty: Medium
Topics  : binary search, math, number theory

## Problem

Fill `arr1` with `uniqueCnt1` distinct positive integers none of which is divisible by `divisor1`, and `arr2` with `uniqueCnt2` distinct positive integers none of which is divisible by `divisor2`, with the two arrays disjoint. Minimize the maximum element across both.

## Approach

Thirteenth on the monotone-predicate-plus-bisect shape, second today. Fix a ceiling `t` and ask whether `1..t` can supply both arrays. Split the range by divisibility:

| class | divisible by | usable by |
| --- | --- | --- |
| reserved for `arr1` | `divisor2` only | `arr1` |
| reserved for `arr2` | `divisor1` only | `arr2` |
| free | neither | either |
| dead | both | nobody |

all four counted by inclusion-exclusion, and feasibility is three inequalities:

```
uniqueCnt1              <= reserved1 + free
uniqueCnt2              <= reserved2 + free
uniqueCnt1 + uniqueCnt2 <= reserved1 + reserved2 + free
```

Minimization, so the feasible set is a suffix and the bisect keeps `mid` on the true half rounding down.

## `O(1)` does not mean invertible

This morning's problem had an expression for a predicate and still had to bisect. I blamed the sum: `sum(c // t)` is written down but it sums over the input, so it is opaque at the level that matters, and I replaced the black-box-versus-expression axis with a count of how many breakpoints you can locate cheaply.

That replacement had an escape hatch. The only `O(1)` predicate the run had ever produced was 1802's, and that one is invertible, so "cheap to evaluate" and "few breakpoints" had never been pulled apart. 2226's predicate is `O(n)`, which leaves the scan available as the explanation and makes the morning's conclusion untested.

**This predicate is `O(1)`.** Three floor divisions, one `gcd`, a comparison. No dependence on anything but the four inputs, and nothing to scan.

And it has a breakpoint at every multiple of `divisor1`, of `divisor2` and of their lcm below the answer, which at the constraint ceiling is millions. There is nothing to invert, and the bisect is not avoidable.

So the two properties come apart on the first case that separates them, in the direction the morning predicted: evaluation cost is not the thing. 1802 inverts because its predicate has *three* pieces, and three is a fact about the tent's geometry, not about how fast the formula runs.

## Hall's condition, and a witness certified without being built

The three inequalities are not three ad hoc necessary conditions that happen to be enough. They are **Hall's condition**. The bipartite graph has two demand nodes, so its subsets are the empty one and the three above, and Hall's theorem says a saturating matching exists exactly when every subset's neighbourhood is large enough. Four subsets, one vacuous, three inequalities, and the theorem makes them sufficient as well as necessary.

That situation has not come up in thirteen problems.

- Nine of the first ten got necessity and sufficiency in one breath, because a greedy built the witness while testing for it. The predicate returning true *was* the construction.
- 2141 got necessity only. The work count proved a run of `t` minutes was not ruled out by total supply, and sufficiency needed a separate schedule with its own argument - the first time the two halves came apart.
- Here nothing is constructed and both halves arrive anyway, because a completeness theorem is doing the work the construction did on the 21st.

So the witness's *existence* is certified without the witness. `minimizeSetAssignment` still builds one, but it is building something already known to be there rather than supplying the proof - and the check on it is a real check for that reason, since a theorem about the graph is not a theorem about the greedy that walks it.

## A third source of canonicity, and the word has been a bucket

Nineteenth day of the summary-versus-set split, and the third distinct reason for canonicity **in one day**.

- 1802: the legal set is closed under pointwise **meet**, so it has a least element.
- 2226 (this morning): the certificate set is closed under pointwise **join**, so it has a greatest one - and the direction is set by which way the constraint's inequality points, not by anything geometric.
- Here: no lattice at all. The witness is a pair of disjoint sets, and pointwise operations on pairs of sets do not preserve the counts, which are equalities rather than bounds.

What makes it canonical instead is that the candidate pool is **totally ordered**. Take the reserved numbers first because nothing else can use them, then fill from the free pool in increasing order. Every choice along the way is between numbers, and numbers come with an order, so "smallest" names a member the way "leftmost" does in 1898.

The 21st separated slack from symmetry. The 22nd added meet-closure as a third thing the word can mean. This is a fourth, and the honest summary is that "canonical" has been a bucket rather than a property for nineteen days - four unrelated mechanisms that all end with a distinguished element and share nothing else.

One caveat kept in the open: filling `arr1` before `arr2` from the free pool is a real choice and it is not forced. The two arrays are not symmetric - their constraints differ - but neither is distinguished by the problem, so the rule is a convention rather than an argument. The tests check the sets are valid rather than checking them against this exact output, which is the split the 21st introduced.

## Bounds

Ninth day, and the bottom end is a third kind.

`t = 1` is not generally feasible, same as this morning. But unlike 2226 there is no zero to fall back to, because the answer is a value in the search space by definition - the problem always has a solution, since the range can always be widened. So the bottom is a range end with no claim attached to it at all, after "feasible by arithmetic" (2141) and "feasible by a promise in the statement" (1802).

The top end is derived rather than guessed. Both divisors are at least 2, so at most half of `[1, t]` is divisible by either one, giving `t - t // divisor >= t / 2` and `t - t // lcm >= t / 2`; all three inequalities then hold at `t = 2 (uniqueCnt1 + uniqueCnt2)`. It is a bound and not a target - it comes from discarding everything except "at least half survives", and it is tight only when both divisors are 2. Fifth day running that the extreme end of the range is not the answer to anything.

## Complexity

Primary: `O(log(uniqueCnt1 + uniqueCnt2))` with an `O(1)` predicate, so about 31 iterations at the constraint ceiling and no dependence on the divisors. Assignment: `O(t)`, and therefore only usable on small inputs, which is why the primary goes nowhere near it. Same-divisor shortcut: one inequality instead of three, kept because it shares no code with `_fits` and so its agreement is a cross-check rather than a restatement.

## Files

- `python/solution.py`
