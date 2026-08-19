# 1898. Maximum Number of Removable Characters

Difficulty: Medium
Topics  : array, string, binary search, two pointers

## Problem

`p` is a subsequence of `s`. `removable` is a list of distinct indices into `s`. Delete `removable[0..k-1]` from `s` and return the largest `k` for which `p` is still a subsequence of what remains.

## Approach

Seventh problem on the monotone-predicate-plus-bisect shape, and the first one where the thing being searched is not a quantity.

The previous six all bisected a number that meant something on its own - a budget, a separation, a per-store load, a day, a gap width - and the monotonicity came from the objective. More budget bought more coverage; waiting longer opened more flowers. The predicate was upward closed because the resource was doing more work at a larger value.

Here `k` is an index into `removable` and nothing else. `removable[3]` is not larger than `removable[1]` in any sense that matters; the array is not sorted and the positions carry no order relation the problem cares about. What `k` indexes is the *set* `removable[:k]`, and those sets are nested by construction:

```
{} ⊂ removable[:1] ⊂ removable[:2] ⊂ ... ⊂ removable
```

"`p` is a subsequence of `s` minus a set" is antitone in the set - taking characters away cannot create a match - so it is antitone along the chain, so it is monotone in `k`. That is the entire monotonicity argument: prefixes nest. No exchange argument, no objective, nothing about what the removals cost.

That is the day. I had been reading *binary search on the answer* as requiring an ordered space of candidate answers with the predicate ordered along it, and the ordered space kept turning out to be the answer's own numeric value - because the problems kept being minimize-a-maximum. What the technique actually needs is a chain and a predicate that is constant on each end of it. A chain of sets is a chain.

The bound at the bottom is not argued, it is promised. `k = 0` is feasible because the problem says `p` is a subsequence of `s`. 1482 is where that stopped being free - the predicate could be false everywhere, the bisect returned a plausible wrong number, and nothing raised - and the fix there was a computed guard. **The guard has not gone away here; it moved into the problem statement.** Drop the promise and this returns `0` for an input with no valid answer at all, in range and silent, which is the 1482 failure exactly. The tests assert the promise rather than trusting it, since it is the only thing holding the bound up.

Direction: this is a maximization, so the true half keeps `mid` and the true half is the one that has to shrink - `mid = (low + high + 1) // 2`, `low = mid`. Not decided by minimize-versus-maximize, which is the thing I got backwards once by reaching for "yesterday was a min so today is a max".

The predicate is the leftmost-match subsequence greedy, and it is easy to forget that it *has* an exchange argument, because the subsequence check is familiar enough to read like a definition. It is not: the claim is that if any embedding of `p` exists then the leftmost one does, proved by pushing each matched position of an arbitrary embedding left to the earliest free slot, which never invalidates a later match since later positions only gain room. Three of the previous six had a real greedy in the predicate and three had a formula. This has a greedy, and it is the first one whose exchange argument was already in hand before the problem started.

The rank form is the alternate and it is the one that says what the search space is. Label each position with the step at which it is deleted - `inf` if never - and "position `i` survives `k` removals" becomes `rank[i] >= k`, a threshold on a label. The chain of nested prefixes collapses into a single function from positions to the time they leave, and the bisect is sweeping a threshold across its range. `removable` stops being an array being consumed and becomes a *labelling* of `s`, which is what it was all along. Kept second anyway, for 1482's reason: the primary should be the transcription of the problem, so that a disagreement between the two is found by the honest one being right.

Attainment, which cost real work three days running, is free here for the first time. 719 needed the boundary to be a jump in the count; 1482 dodged the question by bisecting the input values; 774 could not have it at all, since the answer set was attained but had two billion elements. Here the search space is `{0..n}` and the answer is an index into it by construction, so there is nothing to prove.

Thirteenth day of the summary-versus-set split, and the first canonical witness of the run. The witness set still has slack - `p = "ab"` in `s = "aab"` matches at either `a` - but unlike 2528's unspent budget, 2064's unused stores or 774's inert station, the slack has a **direction**. Embeddings are ordered coordinatewise and a least one exists, so "leftmost" names a specific member and the greedy already computes it. That is the distinction I had been missing for twelve days by filing all of these under *the witness is not canonical*. The question is not whether the witness set has more than one element - it nearly always does - but whether it has a distinguished element. A budget split among tied cities has none, because permuting the cities is a symmetry of the whole problem and there is nothing left to break the tie with. Positions in a string are not symmetric. So for the first time the test checks equality with the leftmost embedding rather than checking a property.

## Complexity

Primary: `O((n + m) log r)` time where `r = len(removable)`, `O(r)` space for the deleted set rebuilt each pass. Rank form: `O(n + r)` setup then `O(n log r)` with no per-pass allocation. Witness: primary plus one scan. Exact-match: `O(n)` for the comparison alone.

## Files

- `python/solution.py`
