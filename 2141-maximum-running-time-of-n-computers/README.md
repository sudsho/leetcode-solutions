# 2141. Maximum Running Time of N Computers

Difficulty: Hard
Topics  : array, greedy, binary search, sorting

## Problem

`n` computers, each needing one battery at a time. Batteries may be swapped between computers at any moment, including fractional ones. Return the largest integer number of minutes for which all `n` can run simultaneously.

## Approach

Tenth on the monotone-predicate-plus-bisect shape, and the first where the predicate proves only half of what it needs to.

The predicate is a work count. Over `t` minutes the `n` computers consume `n * t` battery-minutes, and a battery of capacity `b` can supply `min(b, t)` of them - `min`, not `b`, because it cannot power two computers at the same instant and so cannot give more than `t` however large it is. Feasibility therefore needs `sum(min(b, t)) >= n * t`.

That argument is **necessity and nothing else**. It says a run of `t` minutes cannot happen without enough work available. It does not say the work can be delivered where it is needed. Every one of the previous nine predicates handed me both halves in one breath, because every one of them was a greedy that built the object it was testing for - the scan that counted the balls placed them, the scan that counted the candies chose them. Here the count counts and constructs nothing.

## Monotonicity, without a greedy

The usual argument does not run. For the previous nine I read monotonicity off the greedy: more budget, more room, the scan takes at least as many. Here both sides of the inequality move with `t`, so nothing is settled by inspection.

Write `g(t) = sum(min(b, t)) - n * t`. Each `min(b, t)` is concave in `t`, `-n * t` is linear, so `g` is concave, and `g(0) = 0`. A concave function starting at zero is non-negative on an interval containing `0` and negative outside it, so `{t : g(t) >= 0}` is a prefix. That is the monotonicity, and it comes from concavity rather than from any exchange argument.

First predicate in the run whose monotonicity proof does not mention a greedy. I also got it wrong twice before stating it - both wrong versions were about counting how many batteries sit above the threshold, and the right one is not about counting anything. Both attempts are left in the docstring, because that is the same failure mode as yesterday's bound, which was a correct claim propped up by a sentence about a count.

## Bounds, and the one the assert caught

Sixth day running on bounds, and this pair is genuinely free. `t = 0` needs no work, true by arithmetic rather than by a promise in the statement, which is where 1898's bottom end came from. And `sum(min(b, t)) <= total` for every `t`, so feasibility forces `t <= total / n`.

The assert still caught something. I wrote the top-end check as *the top of the range is feasible*, on the strength of nine days where the extreme threshold was always an achievable configuration. It is not one here. `[100, 1, 1]` with `n = 2` has `total // n = 51`, and only `53` reachable battery-minutes against the `102` such a run would need. The bound comes from dropping the `min()`, and dropping a term gives you a bound and not a witness. So the top end is tested as a bound - the point above it fails - and not as a point.

Smaller than yesterday's, and the same shape: the bound was right, the sentence I justified it with was about something else.

## The third move

The framework these ten days have been building says the search space is generically bigger than the answer set, and which move you get depends on the answer set's size against the cost of the search it would replace. Both branches of that are searches.

This problem has a move that is neither. Sort descending; if the largest battery holds more than the running average `total / n` then no schedule can spend all of it, since the computer it feeds takes at most `t` minutes of it and `t` is at most the average. So it is dedicated, its surplus is unreachable, and the problem drops to `n - 1` computers without it. Otherwise nothing is stranded and the answer is `floor(total / n)`.

The answer set here is `{S_k / (n - k)}` for `k` peeled batteries, `n` candidates, and the scan does not search it. It **identifies** which candidate is the answer, one pass, zero predicate calls, `O(m log m)` and all of that in the sort.

So enumerability was the wrong axis, or at least not the only one. The question is not how big the answer set is; it is whether membership in it is decidable locally. Here it is - battery `i` is peeled iff it exceeds the average of what remains, a test on one element and a running sum - and no amount of counting candidates would have shown that.

## The answer to the 20th, and it is a negative one

On the 20th I wanted a problem in this shape where the answer set is cheaper by an exponent rather than by a constant, on the grounds that ten problems lopsided the same way means I have seen one side of a rule.

There is no such problem, and there cannot be. The range is always a quantity built out of the input's numbers, so its logarithm is bounded by the width of a machine integer - 30 to 60, always, in every problem of this shape I will ever open. The answer set is always indexed by the input, so its size is `n`, which the constraints let run to `1e5` and beyond. `log(range)` is capped by the **format**. `|answer set|` is not.

The lopsidedness is not a property of the ten problems I picked. It is forced, and the comparison I spent ten days building had its result decided before I started.

Third night running that something I was treating as a property of the problem turned out to be relative to something outside it - the representation on the 19th, the alternative on the 20th, the constraint format tonight. This one is worse than the other two, because the outside thing is not part of the mathematics at all. It is an artefact of the venue.

## The witness

Sixteenth day of the summary-versus-set split, and the first where the witness is not a by-product of the predicate.

Sufficiency needs its own construction. Lay the batteries end to end on one timeline of length `n * t`, each contributing `min(b, t)`. Cut into `n` pieces of length `t` and read piece `j` as computer `j`'s schedule. A battery straddling a cut runs computer `j` over `[a, t]` and computer `j + 1` over `[0, x]`, and those clash in wall clock unless `x <= a`. They do not clash, because `x = min(b, t) - (t - a) <= a`. **The cap at `t` is what makes the construction legal, and it is the same cap that made the count correct.** One inequality doing both jobs, which is why I read the predicate as complete on the first pass.

Non-canonical, and this time for symmetry with nothing else mixed in. Permuting the computers is a symmetry of the whole problem - they are interchangeable by definition, not by a coincidence in the input - so the `n!` relabelings are equally good and no rule picks one. That is 2528's tied cities in a purer form.

Which lines up against yesterday exactly. Yesterday was slack with no symmetry available, and the leftmost rule still named a member. Today is symmetry no rule can break, on a problem that has slack too. Two days, the halves separated in both directions, after the 17th ran them together. That is the test I said on the 20th I had only seen one side of, and I got it a day later on a different thread than the one I was asking about.

## Complexity

Primary: `O(m log(total / n))`, one `O(m)` predicate per step. Peeling scan: `O(m log m)`, no predicate calls. Candidate search: `O(m log m + m log n)`. Schedule: primary plus `O(m + n)` intervals. `n == 1`: one pass.

## Files

- `python/solution.py`
