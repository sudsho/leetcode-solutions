import itertools
import random


class Solution:
    def maximumTastiness(self, price, k):
        # ninth on the monotone-predicate-plus-bisect shape, and the first one
        # where i had already written the predicate. this is 1552 with a
        # different noun. there it was baskets on a line and the greedy placed
        # balls left to right keeping a minimum separation; here it is prices on
        # a line and the greedy picks candies left to right keeping a minimum
        # difference. same scan, same monotonicity, same direction. i spent the
        # first ten minutes looking for the part that was new and there isn't
        # one, in the algorithm.
        #
        # so the day is worth something only if the repeat exposes something, and
        # it does, in the place yesterday left open. yesterday's note said the
        # search space is generically bigger than the answer set and there are
        # three things to do about it - repair it at the boundary (719), replace
        # it with the answer set (1482, 2616), or leave it because the answer set
        # is finite and hopeless anyway (774) - and that the property deciding
        # which is available is the *size* of the answer set.
        #
        # this problem's answer set is every pairwise difference. quadratic.
        # finite, enumerable, and completely useless: n is 2e4 so that is 4e8
        # candidates against 30 predicate calls for the plain range search. see
        # maximumTastinessByCandidates for what happens if you build it anyway.
        if k < 2:
            # the statement allows k == 1 and then asks for the minimum absolute
            # difference among the pairs of a one-element basket, of which there
            # are none. taking the empty minimum as 0 rather than letting the
            # search run, which on k == 1 would return max - min for no reason
            # anyone could defend. flagged rather than silently allowed because
            # this is the third time in the run the statement has left a hole at
            # a boundary and the first two times i found it from a test.
            return 0

        price = sorted(price)

        # bounds, and this is the fifth day running i have written this paragraph.
        # gap 0 admits every candy so the count is n and n >= k by constraint,
        # which settles the bottom. i first wrote the top as "gap max - min
        # admits the two ends and nothing between them, count exactly 2" and the
        # test threw it out on [7, 7, 7, 7], where the span is 0, the top and the
        # bottom are the same point and the count is 4. so that sentence is a
        # claim about strictly positive spans and i had stated it unconditionally.
        # the bound itself survives - no basket has a gap above max - min because
        # no *pair* does - and that argument never mentioned the count. fifth day
        # on bounds and the first time the bound was right and my reason for it
        # was wrong, which is worse than the last four, where the reason was
        # missing and visibly so.
        low, high = 0, price[-1] - price[0]

        # maximization, so the true half keeps mid and mid rounds *up*. third
        # maximization in nine and the two before it were 1552 and 1898, so this
        # is not the flip catching me out that it was on the 10th. writing it out
        # anyway, fourth day in a row, because the day i stop is the day i copy
        # yesterday's form into a problem pointing the other way.
        while low < high:
            mid = (low + high + 1) // 2
            if self._count_selectable(price, mid) >= k:
                low = mid
            else:
                high = mid - 1

        return low

    def _count_selectable(self, price, gap):
        """Largest basket whose consecutive prices differ by at least `gap`.

        `price` must already be sorted. Take the first candy, then take each
        later candy whose price is at least `gap` above the last one taken.

        The exchange argument is 1552's and it is one line: if some larger basket
        declines the candy the greedy takes at position `i`, its own next pick
        sits at some `j > i`, and swapping that pick for `i` keeps every later
        gap at least as large, since `price[i] <= price[j]`. Induct rightwards.

        Worth being honest that this is the third of nine predicates with a
        trivial inner greedy, which is what I claimed after 1482 was the pattern
        and then withdrew after 2616 stacked two real exchange arguments in one
        predicate. Both readings survive: the interesting variation in this shape
        really is in the predicate, and the predicate is sometimes free.

        `O(n)` and no allocation.
        """
        count = 1
        last = price[0]

        for value in price[1:]:
            if value - last >= gap:
                count += 1
                last = value

        return count

    def maximumTastinessByCandidates(self, price, k, limit=200):
        """Same search over the pairwise differences instead of over the integers.

        The answer is the smallest consecutive gap inside the chosen basket, so it
        is `price[b] - price[a]` for some pair - attained, exactly as in 2616, and
        for a comparable reason. The difference is the size of the set it is
        attained in: `n - 1` there because the exchange argument collapsed the
        pairing to adjacent positions, and `n * (n - 1) / 2` here because the
        basket is a subsequence and any two of its members can be the tight one.

        **That quadratic is the correction to yesterday.** I filed 774 under
        "answer set finite but hopeless" as though hopeless were a property of the
        number - two billion, obviously too many. It is not. This set has 4e8
        elements at the constraint ceiling, which is smaller than 774's by a
        factor of five and still 600 times worse than simply bisecting the range,
        because the range only costs `log(1e9)` predicate calls. And 2616's
        `n - 1` was not a win because `n - 1` is small; it was a win because
        `n - 1` beat `log(max - min)` on that input.

        So the deciding property is not the answer set's size. It is the answer
        set's size *against the cost of the search it would replace*, and the
        three-way split from yesterday is really two branches and a comparison.
        The "hopeless" branch was never separate - 774 is this problem with a
        worse constant.

        Hence `limit`. Building the set is `O(n^2)` and I will not pretend that is
        a competing implementation on real input; it exists to be run against the
        primary on small cases, where it does test something the primary cannot
        test on itself - that the answer really is attained at a pairwise
        difference. Returns `None` above the limit rather than trying.

        `O(n^2 log n)` to build and sort, then `O(n log n)` for the search.
        """
        if k < 2:
            return 0
        if len(price) > limit:
            return None

        price = sorted(price)
        gaps = sorted(
            {
                price[b] - price[a]
                for a in range(len(price))
                for b in range(a + 1, len(price))
            }
        )

        low, high = 0, len(gaps) - 1
        while low < high:
            mid = (low + high + 1) // 2
            if self._count_selectable(price, gaps[mid]) >= k:
                low = mid
            else:
                high = mid - 1

        return gaps[low]

    def maximumTastinessWitness(self, price, k):
        """Return `(answer, basket)` - the value and the `k` indices realising it.

        `basket` holds indices into the *sorted* array, increasing.

        Fifteenth day of the summary-versus-set split, and the first in a while
        that confirms the rule instead of moving it.

        Yesterday's correction was that canonicity belongs to the space the
        witness is named in rather than to the problem, and that symmetry is what
        removes the distinguished element - I had merely been looking for the
        symmetry in the wrong place. The reason that was only half convincing is
        that back on the 11th I had called slack a separate reason, then decided
        on the 17th it was a confound, because every slack case in that stretch
        happened to be symmetric too.

        This problem separates them, which is the test I have not had. Take
        `[1, 2, 5, 8, 13, 21]` with `k = 3`. The answer is 8, and both
        `(1, 13, 21)` and `(2, 13, 21)` achieve it. The witness set has two
        members and they are not images of each other under any symmetry - the
        prices are all distinct, nothing here is interchangeable. Pure slack, no
        symmetry. And the leftmost greedy still names one of them.

        So slack really does not remove the distinguished element and the 17th was
        right to call it a confound. Six days of cases where it looked like it did
        were six days of cases that were also symmetric.

        Ties in `price` bring back 2616's other half unchanged - equal candies are
        interchangeable, the sort picks between them by input order, and in
        original-index space there is no canonical basket. Same two tests as
        yesterday, for the same reason, on a witness that is a subsequence rather
        than a set of pairs.
        """
        if k < 2:
            return 0, []

        answer = self.maximumTastiness(price, k)
        ordered = sorted(price)

        basket = [0]
        last = ordered[0]
        for i in range(1, len(ordered)):
            if len(basket) == k:
                break
            if ordered[i] - last >= answer:
                basket.append(i)
                last = ordered[i]

        # unreachable - `answer` is feasible, so the scan that decided it finds at
        # least `k` here. raising rather than returning short, for 1482's reason:
        # a predicate and a reconstruction that disagree at the same threshold is
        # the failure that otherwise leaves no symptom at all.
        if len(basket) != k:
            raise AssertionError("feasible gap did not yield k candies")

        return answer, basket

    def maximumTastinessTwo(self, price, k):
        """Shortcut for `k == 2`: the answer is `max - min`.

        Two candies, one gap, nothing to trade off, so take the ends. Same role as
        2616's `p == 1` and 1898's `p == s` - the input where the algorithm makes
        no decision, which makes it the cleanest thing to check the general path
        against. It also pins the top of the range, which random cases reach only
        when `k` happens to come out as 2.

        Returns `None` when it does not apply.
        """
        if k != 2 or len(price) < 2:
            return None

        return max(price) - min(price)


if __name__ == "__main__":
    s = Solution()

    assert s.maximumTastiness([13, 5, 1, 8, 21, 2], 3) == 8
    assert s.maximumTastiness([1, 3, 1], 2) == 2
    assert s.maximumTastiness([7, 7, 7, 7], 2) == 0
    assert s.maximumTastiness([1, 2], 2) == 1
    assert s.maximumTastiness([5], 1) == 0

    cases = [
        ([13, 5, 1, 8, 21, 2], 3),
        ([1, 3, 1], 2),
        ([7, 7, 7, 7], 2),
        ([1, 2], 2),
        ([5], 1),
        ([1, 2, 5, 8, 13, 21], 3),
        ([1, 2, 5, 8, 13, 21], 2),
        ([1, 2, 5, 8, 13, 21], 6),
        ([0, 100], 2),
        ([4, 4, 4, 9, 9, 9], 3),
        ([10, 20, 30, 40, 50], 3),
        ([1, 1, 1, 1, 1, 100], 2),
        ([3, 11, 4, 15, 8, 22, 7], 4),
        ([6, 6, 12, 12, 18, 18], 3),
        ([2, 3, 5, 7, 11, 13, 17], 4),
        ([50, 1, 50, 1, 50, 1], 3),
    ]

    for values, k in cases:
        assert 1 <= k <= len(values), (values, k)

    # both ends of the range, which after five days of writing "the bounds are
    # free here" gets checked rather than asserted in prose. this is the assert
    # that caught me: i wrote the top as admitting exactly the two ends, and on
    # [7, 7, 7, 7] the span is 0, so the top *is* the bottom and admits all four.
    # the condition is what the sentence was missing.
    for values, k in cases:
        ordered = sorted(values)
        span = ordered[-1] - ordered[0]
        assert s._count_selectable(ordered, 0) == len(ordered), values
        if len(ordered) >= 2 and span > 0:
            assert s._count_selectable(ordered, span) == 2, values
        elif len(ordered) >= 2:
            assert s._count_selectable(ordered, span) == len(ordered), values

    # the predicate against its definition rather than through the search. the
    # largest subsequence with all consecutive gaps at least `gap`, computed by
    # brute force over subsets. a predicate that is wrong but still monotone hands
    # back a confident wrong boundary and nothing downstream notices.
    def max_basket_brute(values, gap):
        ordered = sorted(values)
        best = 0
        for size in range(1, len(ordered) + 1):
            for chosen in itertools.combinations(range(len(ordered)), size):
                if all(
                    ordered[b] - ordered[a] >= gap
                    for a, b in zip(chosen, chosen[1:])
                ):
                    best = max(best, size)
        return best

    for values, _ in cases:
        if len(values) > 8:
            continue
        ordered = sorted(values)
        span = ordered[-1] - ordered[0]
        for gap in range(span + 2):
            assert s._count_selectable(ordered, gap) == max_basket_brute(values, gap), (
                values,
                gap,
            )

    # monotonicity, in the direction the bisect uses: the count never rises as the
    # gap grows, so once it drops below k it stays below.
    for values, _ in cases:
        ordered = sorted(values)
        span = ordered[-1] - ordered[0]
        counts = [s._count_selectable(ordered, gap) for gap in range(span + 2)]
        assert all(a >= b for a, b in zip(counts, counts[1:])), values

    # the answer against brute force over all baskets of size k.
    def best_over_all_baskets(values, k):
        if k < 2:
            return 0
        ordered = sorted(values)
        best = 0
        for chosen in itertools.combinations(range(len(ordered)), k):
            worst = min(ordered[b] - ordered[a] for a, b in zip(chosen, chosen[1:]))
            best = max(best, worst)
        return best

    for values, k in cases:
        if len(values) > 8:
            continue
        assert s.maximumTastiness(values, k) == best_over_all_baskets(values, k), (
            values,
            k,
        )

    # attainment: the answer is a pairwise difference. free to check and not free
    # to use, which is the whole of today's note. 2616's version of this assert
    # looked identical and meant something different, because there the set it
    # lands in is the set the alternate search walks.
    for values, k in cases:
        answer = s.maximumTastiness(values, k)
        ordered = sorted(values)
        differences = {
            ordered[b] - ordered[a]
            for a in range(len(ordered))
            for b in range(a + 1, len(ordered))
        }
        assert answer == 0 or answer in differences, (values, k, answer)

    # the candidate-space search agrees where it is affordable to run at all. it
    # shares the predicate and nothing else, so agreement tests attainment
    # constructively rather than restating it.
    for values, k in cases:
        candidate = s.maximumTastinessByCandidates(values, k)
        assert candidate == s.maximumTastiness(values, k), (values, k)

    # and it declines above the limit instead of quietly costing n^2. this is the
    # assert that says the alternate is a test fixture and not an implementation.
    assert s.maximumTastinessByCandidates(list(range(500)), 3) is None
    assert s.maximumTastinessByCandidates(list(range(500)), 3, limit=500) == 249

    # the witness realises the answer exactly. constructive attainment: if every
    # gap in the basket came in strictly above the answer, the same basket would
    # witness answer + 1 and the search would have returned that.
    for values, k in cases:
        answer, basket = s.maximumTastinessWitness(values, k)
        if k < 2:
            assert basket == []
            continue
        ordered = sorted(values)
        assert len(basket) == k, (values, k, basket)
        assert basket == sorted(basket) and len(set(basket)) == k, basket
        gaps = [ordered[b] - ordered[a] for a, b in zip(basket, basket[1:])]
        assert all(gap >= answer for gap in gaps), (values, k, basket)
        assert min(gaps) == answer, (values, k, basket, answer)

    # canonical in sorted-position space - equality against the leftmost greedy
    # computed independently, which is 1898's test and 2616's first half.
    def leftmost_basket(values, k, gap):
        ordered = sorted(values)
        out = [0]
        last = ordered[0]
        for i in range(1, len(ordered)):
            if len(out) == k:
                break
            if ordered[i] - last >= gap:
                out.append(i)
                last = ordered[i]
        return out

    for values, k in cases:
        if k < 2:
            continue
        answer, basket = s.maximumTastinessWitness(values, k)
        assert basket == leftmost_basket(values, k, answer), (values, k, basket)

    # slack without symmetry, which is the case the last six days did not contain.
    # two distinct baskets both achieve 8 on all-distinct prices, so the witness
    # set has more than one member for a reason that is not interchangeability,
    # and leftmost still picks one. asserted directly because the whole point is
    # that both exist.
    ordered = sorted([1, 2, 5, 8, 13, 21])
    assert s.maximumTastiness(ordered, 3) == 8
    for alternative in ((0, 4, 5), (1, 4, 5)):
        gaps = [
            ordered[b] - ordered[a] for a, b in zip(alternative, alternative[1:])
        ]
        assert min(gaps) == 8, alternative
    assert s.maximumTastinessWitness(ordered, 3)[1] == [0, 4, 5]

    # not canonical in original-index space wherever prices tie, unchanged from
    # yesterday. the multiset of prices in the basket is forced; which physical
    # candy carries each price is not, and a stable sort chose by input order. so
    # this half is a property check on the values.
    for values, k in cases:
        if k < 2:
            continue
        answer, basket = s.maximumTastinessWitness(values, k)
        ordered = sorted(values)
        chosen_values = sorted(ordered[i] for i in basket)
        shuffled = list(values)
        random.Random(len(values) * 17 + k).shuffle(shuffled)
        other_answer, other_basket = s.maximumTastinessWitness(shuffled, k)
        other_ordered = sorted(shuffled)
        assert other_answer == answer, (values, shuffled, k)
        assert sorted(other_ordered[i] for i in other_basket) == chosen_values, (
            values,
            shuffled,
            k,
        )

    # k == 2 removes the search, so the general path has to agree with max - min.
    for values, _ in cases:
        if len(values) < 2:
            continue
        assert s.maximumTastiness(values, 2) == s.maximumTastinessTwo(values, 2), values

    assert s.maximumTastinessTwo([1, 2, 3], 3) is None
    assert s.maximumTastinessTwo([1], 2) is None

    # every k from 2 up to n on the same array, so the boundary is walked across
    # rather than sampled. a bigger basket can never be tastier, which is
    # monotonicity of the problem in k rather than of the predicate in the gap -
    # a different claim, and nothing else here would catch it failing.
    for values, _ in cases:
        previous = None
        for k in range(2, len(values) + 1):
            answer = s.maximumTastiness(values, k)
            if previous is not None:
                assert answer <= previous, (values, k, answer, previous)
            assert s.maximumTastinessByCandidates(values, k) == answer, (values, k)
            previous = answer

    # random cases against the brute force. the fixed cases are all hand-picked
    # for a reason and hand-picked cases stop finding things once they pass once.
    rng = random.Random(2517)
    for _ in range(300):
        n = rng.randint(1, 8)
        values = [rng.randint(0, 20) for _ in range(n)]
        k = rng.randint(1, n)
        assert s.maximumTastiness(values, k) == best_over_all_baskets(values, k), (
            values,
            k,
        )
        assert s.maximumTastinessByCandidates(values, k) == s.maximumTastiness(
            values, k
        ), (values, k)

    print("all good")
