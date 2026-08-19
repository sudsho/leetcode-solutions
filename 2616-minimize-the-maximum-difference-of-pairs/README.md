# 2616. Minimize the Maximum Difference of Pairs

Difficulty: Medium
Topics  : array, greedy, binary search

## Problem

Choose `p` pairs of indices from `nums`, no index used twice, and minimise the largest `|nums[i] - nums[j]|` among the chosen pairs. Return that minimum. `p` may be `0`, in which case the answer is `0`.

## Approach

Eighth problem on the monotone-predicate-plus-bisect shape. After yesterday's chain of nested sets the search space is a plain quantity again, so on the surface this is a step back to 2064 or 1552. It is not, and the reason is the loose end from 774 that I wrote down four days ago and did not expect to have answered this fast.

774's note said **attained and enumerable are not the same property**, and that I had been carrying them as one thing. There the answer was provably `d_i / j` for some gap and some `j <= k + 1` — an exact member of a candidate set with two billion elements at the constraint ceiling — so knowing it was attained bought nothing at all. 1482's candidate set was the input array itself, so attainment was free and the question never got asked properly.

Here both halves hold at once, and for a reason rather than by luck. An optimal pairing can always be taken to use pairs that are **adjacent in sorted order**, so the largest difference in it is one of the `n - 1` adjacent gaps. The answer is attained, and the set it is attained in is linear. That is what makes the candidate-space search below an actual alternative rather than a brute force wearing a bisect.

The adjacency argument is an exchange. Take an optimal pairing and two of its pairs whose sorted positions interleave or nest — `a < c < b < d`, or `a < c < d < b`. Re-pair them as `(a, c), (b, d)` in the first case and `(a, b), (c, d)` in the second: the count is unchanged, and in each case both new gaps sit inside the span of the wider old one, so the larger of the two differences cannot go up. Repeat until nothing crosses.

Given adjacency, the predicate is the leftmost-first scan — walk the sorted array, take a pair whenever the next gap fits under the threshold, skip a single element when it does not — and *that* needs its own exchange argument, which is easy to read past because the scan looks obvious. If some solution declines the pair `(i, i+1)` that the greedy takes, it uses at most one of those two positions; drop whichever pair that position belongs to and insert `(i, i+1)`, losing at most one pair and gaining one. Induct rightwards.

So this is the second predicate in eight with a real greedy inside it and the first with **two** exchange arguments stacked — one deciding what the candidate answers are, one deciding how the predicate is computed. Four of the eight have been formulas with nothing to prove, and I had started to believe the exchange argument was never part of the technique. That was 2064 talking.

Both bounds are argued this time, which is worth saying after the last two days. 1482's low end could be false everywhere and needed a computed guard; 1898's low end was promised by the problem statement, so the guard had not disappeared, it had moved somewhere I could not see it. Here neither happens. At `t = max - min` every gap is allowed, the greedy pairs off everything it can reach and returns `floor(n/2)`, and the constraint says `p <= n/2`. The top end is feasible by a counting fact about the input.

Direction: minimisation, so the true half keeps `mid` and `mid` rounds down. Third time writing the rule out instead of reaching for yesterday's form, second time writing it before checking.

## The witness, and a correction

Fourteenth day of the summary-versus-set split, and the first one where *is the witness canonical* has no yes-or-no answer.

Yesterday's conclusion was that the question is not whether the witness set has more than one element — it nearly always does — but whether it has a **distinguished** element, and that what removes the distinguished element is symmetry rather than slack. This problem contains both halves of that at once and they give different answers.

In sorted-position space the witness is canonical, for 1898's reason exactly: positions carry a direction, the scan takes the leftmost pair available at each step, and its first `p` pairs name a specific member of the set. Nothing arbitrary gets chosen.

Map back to the original indices and the canonical choice evaporates wherever `nums` has ties. `[1, 1, 3]` with `p = 1` has exactly one pair in sorted space; in the input there are two equal elements, permuting them is a symmetry of the whole problem, and no rule picks one. The sort picked, and a stable sort picked by an accident of input order.

**So canonicity is not a property of the problem.** It is a property of the space the witness is named in, and sorting is the step that manufactures it — a total order imposed on a multiset that only had a partial one. Symmetry does remove the distinguished element, as of yesterday; the correction is that I had been looking for symmetry in the problem when what matters is whether the representation has already quotiented it away. 2528's tied cities were not more symmetric than these duplicates. They were symmetric in the space I happened to be naming the witness in.

First day in the run where the witness needs two different tests: equality against the leftmost greedy in sorted space, and a property check on the multiset of paired values under a reshuffle of the input.

## Complexity

Primary: `O(n log n)` to sort, then `O(n log(max - min))` for the search. Candidate form: `O(n log n)` to sort and build the gap list, then `O(n log n)` for the search — better on paper, kept second so the transcription stays primary. Witness: primary plus one scan. `p == 1`: `O(n log n)` for the sort and a `min`.

## Files

- `python/solution.py`
