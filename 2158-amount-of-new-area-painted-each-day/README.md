# 2158. Amount of New Area Painted Each Day

Difficulty: Hard
Topics  : array, union find, ordered set, line sweep

## Problem

`paint[i] = [start_i, end_i]` means that on day `i` you paint the half-open span `[start_i, end_i)` of a long strip. Painting an already-painted part does nothing. Return `worklog[i]` = the amount of area painted for the **first time** on day `i`.

## Approach

Yesterday's problem broke the difference array on **composition**. This one breaks it on **attribution**, which is a different failure and worth separating.

Nothing here is order-dependent in the way 699 was. Painting is idempotent, the final painted region is just the union of the intervals, and a difference array will happily report the coverage count of every cell. The coverage count is simply not the answer. The question asks which day reached each cell *first* — an argmin over the days covering it, not a sum over them — and the identity of that first day is precisely what the accumulator destroys when it collapses the days into a number. So the technique is not too slow here; it is answering a different question. That is the sharpest form of the counts-collapse-but-sets-do-not distinction that has decided which alternate was worth keeping in 2251, 2406 and 699.

What rescues it is the one property 699 did not have. The per-cell state is a single bit and it only ever moves unpainted → painted, never back. A cell therefore changes at most once over the entire run, total state changes are bounded by the coordinate range rather than by the number of days, and the only wasted work in the naive version is re-walking cells that are already finished. Skip those and the total becomes linear — which is the whole algorithm. Keep `nxt[i]` = the first unpainted cell at or after `i`, as a union-find in which a painted cell points rightward; painting a cell sets `nxt[i] = i + 1`, and path compression collapses a finished run into a single hop.

The constraints put `end ≤ 5 · 10⁴`, so cells are indexed directly and no coordinate compression is needed. `find` is written iteratively rather than recursively because a compressed chain can span the full coordinate range and would blow Python's recursion limit.

The half-open boundary shows up as the loop condition `cell < end` — painting `[start, end)` covers cells `start … end-1`. Sixth distinct syntax for that same decision in about a week, after the index offset in the array versions, the `bisect_left`/`bisect_right` split in 2251, the strict `<` in 2406 and the `hi - 1` in 699. It still has to be re-derived from the range semantics rather than recalled, and at this point that looks like a property of the technique rather than a gap.

The brute force is the version to write first even though it times out at `10⁵` days over a `5 · 10⁴` range. It states the invariant the fast version is built on: each cell flips `False → True` exactly once across the whole run, so the useful work is bounded no matter how many days arrive, and everything above that bound is re-walking. Written that way the skip pointer stops being a trick.

The third version keeps the painted region as a sorted list of disjoint spans, subtracting the overlap it is not credited for and then splicing the touched run down to one merged span. Scanning is amortized linear — every splice removes `k` spans and inserts one, and only `n` are ever inserted — but the list surgery is `O(n)`, which is why it is not the primary. It earns its place the same way the heap did in 2251 and the skyline in 699: it holds the painted set itself, so it can say *where* a day's new area was, while the union-find can only say how much. A compressed pointer has forgotten which run it skipped over.

## Complexity

Union-find: `O((n + C) α(C))` time and `O(C)` space for `n` days over a coordinate range `C`, effectively linear. Brute force: `O(sum of interval lengths)` time, `O(C)` space. Interval list: amortized `O(n)` scanning but `O(n²)` worst case from the splices, `O(n)` space.

## Files

- `python/solution.py`
