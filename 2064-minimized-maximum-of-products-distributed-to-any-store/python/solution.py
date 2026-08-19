import heapq


class Solution:
    def minimizedMaximum(self, n, quantities):
        # third day on this outer loop and the first one where i can see what
        # it actually is. 2528 and 1552 were both "bisect the answer, the
        # predicate is a greedy left-to-right pass", and both times the whole
        # difficulty was arguing about which way the greedy pushed. two days
        # spent on direction.
        #
        # there is no greedy here at all. the predicate is a sum.
        #
        # so the exchange argument was never part of the technique. it was
        # per-problem baggage that happened to be the hard part twice running,
        # and because it was hard twice i had started filing it under "binary
        # search on the answer" as though it came with the shape. it doesn't.
        # the shape is exactly two things: a monotone predicate, and a bisect
        # that finds its boundary. everything else is whatever it takes to
        # answer the predicate, and today that is one line of arithmetic.
        #
        # the reason it collapses to arithmetic is the store rule. a store
        # carries at most one product type, so the products never compete for
        # the same store and the cost is additive across them. that is the
        # actual gift in the statement and it is easy to read past. if stores
        # could mix, the predicate would be a bin-packing question and none of
        # this would survive.
        #
        # given that, fix product i and ask how well k stores can carry it.
        # spreading q units over k stores leaves the fullest holding at least
        # ceil(q/k) by pigeonhole, and an even split hits exactly that, so the
        # best achievable maximum for one product on k stores *is* ceil(q/k).
        # invert it: ceil(q/k) <= x iff q <= k*x iff k >= ceil(q/x). so holding
        # product i under x costs exactly ceil(q_i/x) stores, no fewer and no
        # search. sum over i, compare against n, done.
        low, high = 1, max(quantities)

        # high is always feasible - sum(ceil(q/max)) is m ones, and m <= n is
        # promised - so the range is nonempty and the answer exists without a
        # guard. second day running that the bound removes a case instead of
        # adding one, and for the same reason both times: the bound is derived
        # from the structure rather than picked large enough to be safe.
        while low < high:
            mid = (low + high) // 2
            if self._fits(n, quantities, mid):
                high = mid
            else:
                low = mid + 1

        return low

    def _fits(self, n, quantities, load):
        """Can `n` stores hold every product with no store carrying more than `load`?

        Each product is independent because a store carries only one type, so
        the cost is a sum rather than an assignment problem, and product `i`
        costs exactly `ceil(q_i / load)` stores.

        Monotone in `load`, which is the part the bisect actually leans on:
        `ceil(q/load)` is non-increasing as `load` grows, so the total is too,
        so the predicate is upward closed. Every previous version of this
        predicate needed an exchange argument before it could be called
        monotone. This one needs the observation that dividing by something
        bigger gives something smaller.

        `-(-q // load)` is the ceiling written as a floor of the negation. The
        usual `(q + load - 1) // load` is the same number but only for positive
        operands, and it reads like a rounding trick rather than a ceiling.
        """
        used = 0

        for q in quantities:
            used += -(-q // load)
            if used > n:
                return False

        return True

    def minimizedMaximumDistribution(self, n, quantities):
        """Return `(answer, stores)` where `stores[i]` is how many stores hold product `i`.

        Ninth day of the summary-versus-set split and the third straight time
        the set turns out not to be canonical, but this is a new reason for it.
        1552's ambiguity was a symmetry - the mirror produced a different
        placement and there was no way to prefer either end. Here it is slack.
        At the optimum `x` the counts only have to sum to at most `n`, so any
        leftover store can be handed to a product that is not the bottleneck.
        Its load drops, the maximum does not move because some other product
        still needs the full `x` (otherwise `x - 1` would have been feasible),
        and the result is a different witness with the same answer.

        So the counts below are the minimal ones rather than the only ones,
        which makes them worth returning and not worth comparing across
        callers. The assertions replay them: sum within budget, every product
        covered, and the tightest even split at those counts landing exactly on
        the claimed answer.
        """
        load = self.minimizedMaximum(n, quantities)
        stores = [-(-q // load) for q in quantities]

        return load, stores

    def minimizedMaximumHeap(self, n, quantities):
        """Same answer by handing out the spare stores one at a time.

        Give every product one store, then repeat `n - m` times: take whichever
        product currently has the worst even-split load and give it one more
        store. The maximum can only come down by relieving whatever is setting
        it, and nothing else in the state changes, so the choice at each step is
        forced rather than argued.

        This is here because it is a genuinely different algorithm and not a
        second copy of the first one. The last two days both ended with two
        callers that shared their inner loop, so agreeing between them was
        weaker evidence than it looked. This one shares nothing with the bisect
        - no predicate, no ceiling-sum, no monotonicity claim - and it still has
        to land on the same number.

        `O(m + (n - m) log m)`, which is worse than the bisect whenever the
        store count dwarfs the product count, and that is the usual case.
        """
        heap = [(-q, q, 1) for q in quantities]
        heapq.heapify(heap)

        for _ in range(n - len(quantities)):
            _, q, k = heapq.heappop(heap)
            k += 1
            heapq.heappush(heap, (-(-(-q // k)), q, k))

        return -heap[0][0]

    def minimizedMaximumSaturated(self, n, quantities):
        """Shortcut for `n == len(quantities)`: every product gets exactly one store.

        There are no spare stores to place, so nothing is being minimized and
        the answer is just the largest quantity. Same role the `m == n` case
        played yesterday - the one input where the algorithm makes no decision,
        which makes it the cleanest thing to check the general path against.

        Returns `None` when the shortcut does not apply, so it cannot be used by
        accident on an input it says nothing about.
        """
        if n != len(quantities):
            return None

        return max(quantities)


if __name__ == "__main__":
    s = Solution()

    assert s.minimizedMaximum(6, [11, 6]) == 3
    assert s.minimizedMaximum(7, [15, 10, 10]) == 5
    assert s.minimizedMaximum(1, [100000]) == 100000
    assert s.minimizedMaximum(22, [25, 11, 29, 6, 24, 4, 29, 18, 6, 13, 25, 30]) == 13
    assert s.minimizedMaximum(2, [1, 1]) == 1

    cases = [
        (6, [11, 6]),
        (7, [15, 10, 10]),
        (1, [100000]),
        (22, [25, 11, 29, 6, 24, 4, 29, 18, 6, 13, 25, 30]),
        (2, [1, 1]),
        (3, [2, 2, 2]),
        (10, [7]),
        (5, [1, 100]),
        (12, [9, 9, 9, 9]),
        (8, [100, 1, 1]),
        (4, [17, 3]),
        (100, [50, 50, 50]),
    ]

    # the heap greedy shares no code and no argument with the bisect - no
    # predicate, no monotonicity - so agreement here is worth more than the
    # two-caller checks the last two days ended on
    for n, quantities in cases:
        assert s.minimizedMaximumHeap(n, quantities) == s.minimizedMaximum(
            n, quantities
        ), (n, quantities)

    # the counts are the minimal witness rather than the only one, so they get
    # replayed - within budget, every product covered, and the even split at
    # those counts landing on the claimed maximum
    for n, quantities in cases:
        load, stores = s.minimizedMaximumDistribution(n, quantities)
        assert sum(stores) <= n, (n, quantities, stores)
        assert all(k >= 1 for k in stores), (n, quantities, stores)
        assert all(-(-q // k) <= load for q, k in zip(quantities, stores)), (
            n,
            quantities,
            stores,
        )
        assert max(-(-q // k) for q, k in zip(quantities, stores)) == load, (
            n,
            quantities,
            stores,
        )

    # no spare stores means no decision, so the general path has to agree with
    # the plain maximum
    for quantities in [[11, 6], [15, 10, 10], [100000], [9, 9, 9, 9], [1, 100]]:
        expected = s.minimizedMaximumSaturated(len(quantities), quantities)
        assert s.minimizedMaximum(len(quantities), quantities) == expected, quantities

    assert s.minimizedMaximumSaturated(5, [1, 2]) is None

    # and the exhaustive check over every way to split the stores, which is the
    # only one that tests the ceil(q/k) lemma rather than the search around it
    def brute(n, quantities):
        m = len(quantities)
        best = [None]

        def walk(i, left, worst):
            if best[0] is not None and worst >= best[0]:
                return
            if i == m:
                best[0] = worst
                return
            # leave at least one store for each product still to come
            for k in range(1, left - (m - i - 1) + 1):
                walk(i + 1, left - k, max(worst, -(-quantities[i] // k)))

        walk(0, n, 0)
        return best[0]

    for n, quantities in [
        (6, [11, 6]),
        (7, [15, 10, 10]),
        (2, [1, 1]),
        (3, [2, 2, 2]),
        (5, [1, 100]),
        (12, [9, 9, 9, 9]),
        (8, [100, 1, 1]),
        (4, [17, 3]),
        (9, [13, 7, 5]),
        (11, [30, 12, 8, 3]),
    ]:
        assert s.minimizedMaximum(n, quantities) == brute(n, quantities), (n, quantities)

    print("all good")
