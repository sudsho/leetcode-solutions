from bisect import bisect_left


class Solution:
    def amountPainted(self, paint):
        # second way the accumulator fails, and it fails for a completely
        # different reason than yesterday's.
        #
        # 699 broke on composition: the update read the state it was about to
        # write, and it wrote an assignment, so two updates in the other order
        # gave a different answer and there was nothing to accumulate. that is
        # not the problem here. painting is idempotent and order-independent
        # at the level of the final picture - after all n days the painted set
        # is just the union of the intervals, and a diff array computes the
        # coverage count of every cell without breaking a sweat.
        #
        # the coverage count is simply not the answer. the question is which
        # day painted each cell FIRST, and that is an argmin over the days
        # covering a cell, not a sum over them. the accumulator collapses the
        # days into a number and the identity of the first one is exactly what
        # gets destroyed in the collapse. so this is not "the technique is too
        # slow", it is "the technique answers a different question" - the
        # sharpest version of the counts-collapse-but-sets-do-not line that has
        # decided which alternate was worth keeping in 2251, 2406 and 699.
        #
        # what makes it tractable anyway is the one property 699 did not have.
        # the per-cell state here is a single bit and it only ever goes
        # unpainted -> painted, never back. so a cell changes at most once over
        # the whole run, total state changes are bounded by the coordinate
        # range, and the only wasted work in the naive version is re-walking
        # cells that are already done. skip them and the total is linear.
        #
        # nxt[i] is the first unpainted cell at or after i, maintained as a
        # union-find where a painted cell points rightward. constraints put
        # end <= 5 * 10^4, so cells are indexed directly - no compression, and
        # cell i means the half-open span [i, i+1). painting [start, end)
        # covers cells start .. end-1, which is where the half-open boundary
        # lives this time: the loop is `i < end`, not `i <= end`. sixth syntax
        # for that same decision in about a week and it still has to be
        # re-derived from the range semantics rather than recalled.
        limit = max(end for _, end in paint)
        nxt = list(range(limit + 1))

        def find(cell):
            # two-pass path compression, iterative because the chain can be
            # the full coordinate range and python's recursion limit is 1000.
            root = cell
            while nxt[root] != root:
                root = nxt[root]
            while nxt[cell] != root:
                nxt[cell], cell = root, nxt[cell]
            return root

        answer = []
        for start, end in paint:
            fresh = 0
            cell = find(start)
            while cell < end:
                fresh += 1
                # this cell is done forever; send anyone landing here onward.
                nxt[cell] = cell + 1
                cell = find(cell + 1)
            answer.append(fresh)

        return answer

    def amountPaintedBrute(self, paint):
        """O(total interval length): walk every cell of every interval.

        Too slow on the real constraints - 10^5 days over a range of 5 * 10^4
        is up to 5 * 10^9 cell visits - but it is the version worth writing
        first because it states the invariant the fast one is built on. Each
        cell flips False -> True exactly once across the entire run, so the
        useful work is bounded by the coordinate range no matter how many days
        there are. Everything above that bound is re-walking cells that were
        already painted, and that is the only thing the union-find removes.
        """
        limit = max(end for _, end in paint)
        painted = [False] * limit
        answer = []

        for start, end in paint:
            fresh = 0
            for cell in range(start, end):
                if not painted[cell]:
                    painted[cell] = True
                    fresh += 1
            answer.append(fresh)

        return answer

    def amountPaintedIntervals(self, paint):
        """Keep the painted region as a sorted list of disjoint spans.

        Each day finds the spans its interval touches, subtracts the overlap
        it is not credited for, then splices the whole run down to one merged
        span. Every splice removes k spans and inserts 1, and only n spans are
        ever inserted, so the scanning is amortized linear - the list surgery
        is the O(n) part and the reason this is not the primary version.

        It is worth keeping for the usual reason: it holds the painted set
        itself rather than a count of it. The union-find can say how much was
        new on day i but not where, because a compressed pointer has forgotten
        which run it skipped over. If the follow-up asked which segments a day
        actually contributed, or wanted the painted region reported at the end,
        this version already has it and the union-find would have to be rebuilt
        from the input to answer.

        Adjacent spans are merged too (`>=` and `<=` rather than strict), which
        costs nothing - a zero-width overlap subtracts zero - and keeps the
        list from filling with spans that touch but never coalesce.
        """
        covered = []  # sorted, disjoint, half-open (start, end)
        answer = []

        for start, end in paint:
            idx = bisect_left(covered, (start,))
            # the span before idx starts earlier; it still counts if it reaches
            # start, so back up one and let the scan below handle it.
            if idx and covered[idx - 1][1] >= start:
                idx -= 1

            fresh = end - start
            merged_start, merged_end = start, end
            j = idx
            while j < len(covered) and covered[j][0] <= end:
                span_start, span_end = covered[j]
                # covered spans are disjoint, so the overlaps never double count
                fresh -= max(0, min(span_end, end) - max(span_start, start))
                merged_start = min(merged_start, span_start)
                merged_end = max(merged_end, span_end)
                j += 1

            covered[idx:j] = [(merged_start, merged_end)]
            answer.append(fresh)

        return answer
