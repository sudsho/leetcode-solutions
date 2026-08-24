# 2439. Minimize Maximum of Array

Difficulty: Medium
Topics  : array, prefix sum, greedy, binary search, math

## Problem

Given a 0-indexed array `nums` of non-negative integers, repeatedly pick an index `i` in `[1, n-1]` with `nums[i] > 0`, decrease `nums[i]` by 1 and increase `nums[i-1]` by 1. Return the minimum possible value of the maximum element.

## Approach

Units move left and only left, so for any prefix `[0..i]` the total inside it can gain from the right and can never lose. That gives the reachability relation:

```
b reachable from a  <=>  b >= 0, sum(b) == sum(a),
                         and prefix_b[i] >= prefix_a[i] for every i
```

Every entry being at most `t` gives `prefix_b[i] <= (i+1) t`, so a ceiling `t` is feasible exactly when

```
prefix_a[i] <= (i + 1) * t        for every i
```

and the answer is `max over i of ceil(prefix[i] / (i+1))`. One pass, no search.

## The bisect does not happen, and that is the whole day

Fourteenth on the monotone-predicate-plus-bisect shape and the first one where nothing is searched.

The last two days were an argument about what makes a predicate invertible. On the 23rd I proposed expression-versus-black-box, discarded it within a day because 2226's predicate is an expression and still has to be searched, and replaced it with a count of cheaply locatable breakpoints. 2513 then produced an `O(1)` predicate with millions of breakpoints, which killed evaluation cost as the axis and left the breakpoint count standing.

The breakpoint count is wrong too. This predicate is a conjunction of `n` terms, so it has up to `n` breakpoints - more than 1802's three and nowhere near "few" - and it inverts anyway, because a conjunction of constraints each solvable for `t` is just a max of the solved forms.

So the axis is not the number of breakpoints. It is two independent properties:

| | predicate | shape | inverts |
| --- | --- | --- | --- |
| 1802 | tent sum vs budget | conjunction of 3, each quadratic in `t` | yes |
| 2226 | `sum(c // t) >= k` | an **aggregate** - terms coupled by the sum | no |
| 2513 | Hall, three counts | conjunction of 3, each floor-heavy | no |
| 2439 | `prefix[i] <= (i+1) t` | conjunction of `n`, each linear | yes |

The predicate has to be a conjunction rather than an aggregate, **and** the individual terms have to be solvable. The run has now produced a failure of each kind separately, one on each of the last two days, which is why the breakpoint count tracked the truth on the four cases I had - it was a proxy for the pair of them.

## Join-closure again, on a different object

Twentieth day of the summary-versus-set split, and the first mechanism to repeat.

Four problems gave four reasons for a canonical witness - a leftmost convention (1898), meet-closure (1802), join-closure (2226), a total order with no lattice anywhere (2513) - and yesterday I wrote that "canonical" had been a bucket rather than a property. This is 2226's mechanism a second time.

What is new is the object it acts on. 2226's join was on certificates. Here it is on **prefix vectors**: pointwise max preserves non-decreasing, preserves `>= prefix_a`, and preserves the step bound, since if the max at `i` comes from `P` then `max(P,Q)[i] - max(P,Q)[i-1] <= P[i] - P[i-1] <= t`. So the feasible set has a greatest element, `prefix_final[i] = min((i+1) t, total)` - push every unit as far left as the ceiling allows.

And the optimum is genuinely not unique. `[0, 3]` has answer 2 with both `[2, 1]` and `[1, 2]` attaining it, and those two arrays are incomparable. They are not incomparable as prefix vectors. The order that makes the choice canonical is on the prefixes and not on the thing the problem asks about, which did not come up in the previous four because there the witness and the ordered object were the same thing.

## Bounds

Tenth day, and the section is empty.

Nine days of a bottom end and a top end, three kinds of bottom and two of top, and today there is no interval to bracket. The cross-check bisect needs one and gets `[0, max(nums)]` - zero is feasible exactly when every entry is zero, `max(nums)` is feasible because doing nothing attains it - but that is a range for the check and not for the answer.

For nine days "what are the bounds" felt like a question about the problem. It is a question about the method.

## Complexity

Primary: `O(n)` time, `O(1)` space. Cross-check bisect: `O(n log(max nums))`. Witness: `O(n)`. The BFS over the reachable set in the test block is exponential and only runs on inputs of five entries or fewer, which is deliberate - it is the only thing in the file that touches the moves rather than the prefix characterisation, so everything else would pass unchanged if that characterisation were wrong.

## Files

- `python/solution.py`
