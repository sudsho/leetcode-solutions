# 1526. Minimum Number of Increments on Subarrays to Form a Target Array

Difficulty: Hard
Topics  : array, dynamic programming, greedy, monotonic stack, prefix sum

## Problem

Start from an all-zero array the same length as `target`. One operation picks any subarray and adds `1` to every element of it. Return the minimum number of operations needed to turn the zero array into `target`.

## Approach

Every problem in this family so far has run the map one way: here is a pile of range updates, report the array they accumulate to. This one hands over the accumulated array and asks for the cheapest pile of range updates that produces it. Same map, read backwards.

That the backwards question is even well-posed is the part worth keeping. The difference array is a bijection. An array of length `n` with an implied `0` boundary determines its delta sequence and the delta sequence determines it back, which is precisely why the accumulate step loses nothing and why two writes are allowed to stand in for a whole range. That fact has been doing quiet background work all week. Here it *is* the problem.

An operation on `[l, r]` contributes `+1` to `d[l]` and `-1` to `d[r+1]`, and nothing else. The required `d` is pinned down by the target. So

```
d[i] = (operations starting at i) - (operations ending at i-1)
```

and the subtracted term is never negative, so at least `d[i]` operations must start at `i` whenever `d[i] > 0`. Every operation starts somewhere exactly once, which makes the total at least the sum of the positive deltas. Answer: `target[0] + sum(max(0, target[i] - target[i-1]))`.

What makes that feel like a different kind of argument than the rest of the week is that nothing is simulated to reach it. There is no sweep and no state. The count is forced by the structure of what a single update is permitted to write, and the lower bound falls out before any construction exists. The negative deltas never cost anything, because a close can always be paired against an already-open start, so only opens are ever paid for.

`target[0]` is the leading term because `d[0] = target[0] - 0`. The zero boundary is not a special case here either. It is the same implied value that put the closing write one past the end all week.

The divide-and-conquer version is the one found first: apply the full-width subarray `min - base` times, then every position holding that minimum is finished and the range splits into independent pieces between them. It is `O(n²)` as written since the minimum is rescanned, `O(n log n)` with a sparse table, and the three-line answer beats both. It stays because it knows *why* each operation exists. Each `min - base` is a real stack of subarrays over a real range, and the linear version has already collapsed that into a number.

That is the fifth time this week the summary-versus-set distinction has decided whether an alternate earns its place, after 2251, 2406, 699 and 2158. The difference is that in all four of those it was justifying a slower structure against a hypothetical follow-up. Here the fast version is three lines with no structure in it at all, so the alternate is the only thing standing between the answer and an unexplained number.

The third version builds the operations instead of counting them, which is the achievability half of the bound written out rather than asserted. It walks the same deltas: a positive delta opens that many operations and pushes their starts, a negative delta closes that many, most recent first. LIFO is correct and not just convenient, since two operations over one delta sequence are either nested or disjoint and never cross, so the stack is never choosing. It is `O(answer)` rather than `O(n)`, which matters when the target is `10⁵` everywhere.

## Complexity

Primary: `O(n)` time, `O(1)` space. Divide and conquer: `O(n²)` worst case as written, `O(n log n)` with range-minimum preprocessing. Construction: `O(answer)` time and space.

## Files

- `python/solution.py`
