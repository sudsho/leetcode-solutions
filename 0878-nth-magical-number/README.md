# 878. Nth Magical Number

Difficulty: Hard
Topics  : math, number theory, binary search, gcd/lcm

## Problem

A positive integer is *magical* if it is divisible by `a` or by `b`. Given `n`, `a` and `b`, return the `n`-th smallest magical number, modulo `10^9 + 7`.

Constraints: `1 <= n <= 10^9`, `2 <= a, b <= 4 * 10^4`.

## Approach

Counting is inclusion-exclusion. With `L = lcm(a, b)`,

```
count(t) = t//a + t//b - t//L
```

is the number of magical numbers in `[1, t]`, and the answer is the least `t` with `count(t) >= n`.

Since `a | L` and `b | L`, every term steps by a fixed amount when `t` moves by a whole period:

```
count(t + L) = count(t) + (L//a + L//b - 1) = count(t) + P     for every t
```

So write `n = qP + r`. If `r == 0` the answer is `q L` - the last magical number of the `q`-th period is the boundary itself, since `L` is a multiple of both. Otherwise it is `q L` plus the `r`-th magical number inside one period, found by a two-pointer merge of the multiples of `a` and of `b` in `(0, L]`. That merge has `L//a + L//b - 1 = b/g + a/g - 1` steps, so the whole thing is `O(a + b)` and does not scale with `n` at all.

## An aggregate that inverts, which yesterday's rule says cannot happen

Fifteenth on the monotone-predicate-plus-bisect shape, and the second in a row where nothing is searched. Yesterday that was the headline; today it is the setup.

Yesterday's rule was that inverting a predicate needs two things: the predicate has to be a **conjunction** rather than an aggregate, and the individual terms have to be solvable. This predicate is an aggregate. Not loosely - it is a sum of floor terms with the terms coupled by the summation, the same object as 2226's `sum(c // t) >= k`, floors and all. By yesterday's rule it does not invert.

It inverts exactly, in `O(a + b)`, and not by decomposing the sum, because the sum does not decompose. It inverts because the predicate is **equivariant**: it commutes with translation by `L` up to a constant. That is a property of the aggregate as a whole and it says nothing about the individual terms.

Fourth candidate axis in four days, fourth one dead inside a day:

| written | proposed axis | killed by |
| --- | --- | --- |
| 22nd | expression vs black box | 2226, on the 23rd |
| 23rd | count of cheaply locatable breakpoints | 2513, the same night |
| 24th | conjunction, and each term solvable | 0878, today |

The pattern in the failures is the useful part. Each candidate was one **handle** promoted to a general condition, and what the run has actually been accumulating is a list whose entries have nothing in common:

- algebraic separability - 1802, 2439
- an exchange argument shrinking the answer set - 2616, 2517
- local decidability of membership - 2141
- a symmetry of the predicate - 0878

Bisection is what you do with a predicate that offers exactly one handle, evaluation at a point. Anything else it offers is a shortcut, and the shortcuts are unrelated to each other. "Invertible" was never a property of a predicate; it was a name for *some handle exists*, and four days were spent trying to give a single name to the disjunction of an open list.

## Two certificates, one object

Twenty-first day of the summary-versus-set split, and a mechanism that has not appeared before.

A certificate that `t` is magical is a divisor witness, `(a, t//a)` or `(b, t//b)`. A `t` divisible by both has **two certificates for one object**, so `t//a + t//b` counts certificates and not objects. Every previous day in this thread resolved multiplicity by *choosing* one - a leftmost convention (1898), a meet (1802), a join (2226 and 2439), a total order on the candidate pool (2513). Here nothing is chosen. The duplicates are counted and subtracted, which is available only because the double-covered set is as easy to count as the covers are, and `- t//L` is that subtraction.

The two-pointer merge does the same correction geometrically: when the two pointers land on the same value it advances both. Forgetting that is the same bug as dropping the third term of the inclusion-exclusion.

## Bounds

Eleventh day, and unlike yesterday there is a range to state. The bottom is `min(a, b)`, attained at `n = 1`. The top is `n * min(a, b)`, since the first `n` multiples of the smaller are already `n` distinct magical numbers - a bound with nothing attaining it in general (`n = 3, a = 2, b = 3` has a ceiling of 6 and an answer of 4), fourth day running for that.

What is new is the width. Ten days of ranges built out of the input's array entries, so `log(range)` was capped by the width of a machine integer - the 21st's conclusion, and the reason the range side of the range-vs-answer-set comparison could never lose by an exponent. Here the search space is genuinely unbounded above and the conclusion survives anyway: `n` is an input too, so `n * min(a, b)` is about `4 * 10^13` and its log is about 45. The argument never needed the range to come from array entries, only from *some* input, which is weaker than what I wrote it as.

The answer set is the second half of that comparison and it does not survive. On the 21st I wrote that the answer set is always indexed by the input, so its size is `n` and `n` runs to `10^5`. The answer set here is the magical numbers, which is infinite. What is enumerated is the **quotient** by the translation, of size `P <= a/g + b/g`, and that is bounded by the input's *values* rather than by any input length. First problem in the run where enumerating the answer set means enumerating a quotient of it.

## Complexity

Primary: `O(a + b)` time - specifically `O(a/g + b/g)` merge steps with `g = gcd(a, b)` - and `O(1)` space, independent of `n`. Cross-check bisect: `O(log(n * min(a, b)))` predicate calls, each `O(1)`. Brute force in the test block tests every integer up to a few thousand and is the only route in the file that mentions neither the lcm nor the period, so everything else would pass unchanged if the equivariance argument were wrong.

The modulus is applied once, at the very end. `_exact` returns the true integer because every claim in the test block is about the ordering of the magical numbers and a residue has no ordering - `count(answer) >= n` asserted against a reduced value asserts nothing, and the true answer reaches `2 * 10^13`.

## Files

- `python/solution.py`
