import itertools
import random


class Solution:
    def minimizeMax(self, nums, p):
        # eighth problem on the monotone-predicate-plus-bisect shape. the search
        # space is a quantity again after yesterday's chain of sets, so on the
        # surface this is a step back to 2064 or 1552. it isn't, and the reason
        # is the leftover from 774 that i wrote down four days ago and did not
        # expect to get answered this quickly.
        #
        # 774's note said attained and enumerable are not the same property, and
        # i had been carrying them as one. there the answer was provably some
        # d_i / j, an exact member of a candidate set with two billion elements,
        # so knowing it was attained bought nothing. 1482's candidate set was the
        # input itself, n elements, so there attainment came for free and the
        # question never got asked properly.
        #
        # here both halves are true at once and for a reason. the optimal pairing
        # can always be taken to use pairs that are adjacent in sorted order (the
        # exchange argument is in _count_pairs), so the maximum difference in it
        # is one of the n-1 adjacent gaps. the answer is attained *and* the set it
        # is attained in has n-1 elements. that is the first time in the run the
        # candidate set has been small enough to bisect over directly while still
        # being an argument rather than a coincidence, and the alternate below
        # does exactly that.
        if p == 0:
            return 0

        nums = sorted(nums)

        # both ends are argued here, which is worth saying out loud after the
        # last two days. 1482's low end could be false everywhere and needed a
        # computed guard; 1898's low end was promised by the problem statement
        # and the guard had merely moved somewhere i could not see it. this one
        # is neither. at t = max - min every adjacent gap is allowed, so the
        # greedy pairs off every element it can reach and returns floor(n/2)
        # pairs, and the constraint says p <= n/2. the top bound is feasible by
        # a counting argument over the input, not by assumption.
        low, high = 0, nums[-1] - nums[0]

        # minimization, so the true half keeps mid and mid rounds down. third
        # time i have written the rule out rather than reached for the previous
        # day's form, and the second time i wrote it before checking.
        while low < high:
            mid = (low + high) // 2
            if self._count_pairs(nums, mid) >= p:
                high = mid
            else:
                low = mid + 1

        return low

    def _count_pairs(self, nums, threshold):
        """How many disjoint pairs with difference `<= threshold` fit in `nums`?

        `nums` must already be sorted. Left to right, take a pair whenever the
        next gap fits and skip a single element when it does not.

        Two exchange arguments hide in three lines here and both are easy to read
        past, which is the thing worth slowing down for. Four of the previous
        seven predicates were formulas with nothing to prove and one - 1898's
        subsequence check - had a greedy whose argument I already knew. This one
        needs both halves stated.

        First, only adjacent pairs matter. Take an optimal pairing and two of its
        pairs whose sorted positions interleave or nest, `a < c < b < d` or
        `a < c < d < b`. Re-pairing them as `(a, c)` and `(b, d)`, or `(a, b)` and
        `(c, d)` respectively, leaves the count alone and cannot raise the larger
        of the two differences, since in each case both new gaps sit inside the
        span of the old wider one. Repeat until nothing crosses; what is left is
        a set of pairs adjacent in sorted order. **This is what makes the answer
        one of the `n - 1` gaps**, and the whole reason the candidate form below
        exists.

        Second, given that, the leftmost-first scan is optimal for the count.
        Suppose some solution skips the pair `(i, i + 1)` that the greedy takes.
        It uses at most one of those two positions, so removing whichever pair
        that position belongs to and inserting `(i, i + 1)` costs at most one
        pair and gains one. Induct rightwards on what remains.

        `O(n)` per call and no allocation, which is the reason this is the
        primary and the candidate form is not.
        """
        count = 0
        i = 0

        while i + 1 < len(nums):
            if nums[i + 1] - nums[i] <= threshold:
                count += 1
                i += 2
            else:
                i += 1

        return count

    def minimizeMaxByCandidates(self, nums, p):
        """Same search, run over the gaps themselves instead of over the integers.

        The adjacency argument in `_count_pairs` says the answer is one of the
        differences between neighbours in sorted order, so the search space can
        be that list of `n - 1` numbers rather than the range `[0, max - min]`.
        Bisect the index into it and what comes back is an exact member of the
        candidate set rather than a number that happens to equal one.

        This is 1482's value-space form, and there I kept it second because it
        was a shortcut that the problem happened to allow - the candidate set was
        the input array, so it needed no argument and taught nothing. Here it
        needs the exchange argument to exist at all, and running it *is* the test
        of that argument: if adjacency were wrong the two searches would disagree
        on some input, and they are checked against each other below on every
        case rather than spot-checked.

        774 is the contrast that makes this worth writing down. There the answer
        was also provably a member of a candidate set - `d_i / j` for some gap and
        some `j <= k + 1` - and the set had `|gaps| * (k + 1)` elements, two
        billion at the constraint ceiling. Attained, not enumerable, and the
        candidate form was a brute force on toy inputs. The difference is not the
        problem being easier. It is that the exchange argument here collapses the
        candidates down to a linear-sized set before the search starts.

        `O(n log n)` for the sort, then `log n` predicate calls instead of
        `log(max - min)`. Better on paper and second anyway, for 1482's reason:
        the primary should be the transcription, so a disagreement between the
        two is found by the honest one being right.
        """
        if p == 0:
            return 0

        nums = sorted(nums)
        gaps = sorted({nums[i + 1] - nums[i] for i in range(len(nums) - 1)})

        low, high = 0, len(gaps) - 1
        while low < high:
            mid = (low + high) // 2
            if self._count_pairs(nums, gaps[mid]) >= p:
                high = mid
            else:
                low = mid + 1

        return gaps[low]

    def minimizeMaxWitness(self, nums, p):
        """Return `(answer, pairs)` - the value and the `p` pairs that realise it.

        `pairs` holds indices into the *sorted* array, in increasing order, and
        each one is an adjacent pair.

        Fourteenth day of the summary-versus-set split, and the first one where
        the answer to "is the witness canonical" is neither yes nor no.

        Yesterday's 1898 note said the question is not whether the witness set has
        more than one element but whether it has a distinguished element, and that
        what removes the distinguished element is symmetry rather than slack.
        This problem contains both halves of that at once and they disagree.

        In sorted-position space the witness is canonical, and for 1898's reason
        exactly: positions carry a direction, the greedy scan takes the leftmost
        pair available at every step, and the first `p` pairs it produces are a
        specific member of the set. Nothing arbitrary is chosen.

        Map it back to the original indices and the canonical choice evaporates
        wherever `nums` has ties. `[1, 1, 3]` with `p = 1` pairs the two `1`s and
        there is exactly one such pair in sorted space; in the input there are two
        equal elements and permuting them is a symmetry of the entire problem, so
        no rule picks one. The sort chose, and a stable sort chose by an accident
        of input order.

        So canonicity is not a property of the problem. It is a property of the
        space the witness is named in, and sorting is the step that manufactures
        it - a total order imposed on a multiset that only had a partial one. That
        is the correction to yesterday. Symmetry does remove the distinguished
        element, and I had been checking for symmetry in the problem when the
        thing that matters is whether the representation has already quotiented it
        away.

        The tests below check both readings, which is the first time in the run
        that the witness has needed two different tests: equality against the
        leftmost greedy in sorted space, and a property check in original-index
        space when there are ties.
        """
        if p == 0:
            return 0, []

        order = sorted(range(len(nums)), key=lambda i: nums[i])
        ordered = [nums[i] for i in order]
        answer = self.minimizeMax(nums, p)

        pairs = []
        i = 0
        while i + 1 < len(ordered) and len(pairs) < p:
            if ordered[i + 1] - ordered[i] <= answer:
                pairs.append((i, i + 1))
                i += 2
            else:
                i += 1

        # unreachable - `answer` is feasible, so the same greedy that decided it
        # finds at least `p` pairs here. raising rather than returning short: a
        # fall-through would mean the predicate and this scan disagree at the same
        # threshold, which is the failure 1482 taught me is otherwise silent.
        if len(pairs) != p:
            raise AssertionError("feasible threshold did not yield p pairs")

        return answer, pairs

    def minimizeMaxAllDistinctGaps(self, nums, p):
        """Shortcut for `p == 1`: the answer is the smallest adjacent gap.

        One pair to place and no interaction between choices, so the greedy, the
        exchange argument and the search all collapse into a `min` over the gaps.

        Same role as 1898's `p == s` and 1482's `k == 1` - the input where the
        algorithm makes no decisions at all, so it is the cleanest thing to check
        the general path against. It also lands on the bottom end of the range,
        which the random cases reach only when they happen to contain a duplicate.

        Returns `None` when it does not apply, so it cannot be used by accident on
        an input it says nothing about.
        """
        if p != 1 or len(nums) < 2:
            return None

        nums = sorted(nums)

        return min(nums[i + 1] - nums[i] for i in range(len(nums) - 1))


if __name__ == "__main__":
    s = Solution()

    assert s.minimizeMax([10, 1, 2, 7, 1, 3], 2) == 1
    assert s.minimizeMax([4, 2, 1, 2], 1) == 0
    assert s.minimizeMax([3, 4, 2, 3, 2, 1, 2], 3) == 1
    assert s.minimizeMax([0], 0) == 0
    assert s.minimizeMax([5, 5], 1) == 0

    cases = [
        ([10, 1, 2, 7, 1, 3], 2),
        ([4, 2, 1, 2], 1),
        ([3, 4, 2, 3, 2, 1, 2], 3),
        ([0], 0),
        ([5, 5], 1),
        ([1, 1, 1, 1], 2),
        ([1, 5, 9, 13], 2),
        ([1, 2, 3, 4, 5, 6], 3),
        ([1, 2, 3, 4, 5, 6], 1),
        ([0, 100], 1),
        ([7, 7, 7, 1, 1, 1], 3),
        ([2, 9, 4, 11, 6, 13], 2),
        ([1, 3, 6, 19, 20], 2),
        ([8, 8, 9, 9, 10, 10], 3),
        ([31, 2, 17, 4, 29, 6], 3),
        ([0, 0, 0, 0, 0, 0, 0, 0], 4),
    ]

    for values, p in cases:
        assert 0 <= p <= len(values) // 2, (values, p)

    # the top bound is argued rather than assumed, so it gets checked. this is
    # the 1482 guard and it lives at the other end this time: the search is only
    # correct because the predicate is true somewhere, and here that is a
    # counting fact about the input rather than a promise from the statement.
    for values, p in cases:
        if p == 0:
            continue
        ordered = sorted(values)
        assert s._count_pairs(ordered, ordered[-1] - ordered[0]) >= p, (values, p)
        assert s._count_pairs(ordered, ordered[-1] - ordered[0]) == len(values) // 2

    # the predicate against its definition, directly - the maximum number of
    # disjoint pairs under a threshold, computed without the greedy. a predicate
    # that is wrong but still monotone hands back a confident wrong boundary with
    # no symptom, which is why this is not checked through the search.
    def max_pairs_brute(values, threshold):
        ordered = sorted(values)
        n = len(ordered)
        best = [0] * (n + 1)
        for i in range(n - 2, -1, -1):
            take = 0
            if ordered[i + 1] - ordered[i] <= threshold:
                take = 1 + best[i + 2]
            best[i] = max(take, best[i + 1])
        return best[0]

    for values, _ in cases:
        ordered = sorted(values)
        span = ordered[-1] - ordered[0]
        for t in range(span + 2):
            assert s._count_pairs(ordered, t) == max_pairs_brute(values, t), (values, t)

    # monotonicity of the count in the threshold, which every search assumes and
    # none of them would notice failing. stated in the direction the bisect uses:
    # once the count clears p it never drops back.
    for values, _ in cases:
        ordered = sorted(values)
        span = ordered[-1] - ordered[0]
        counts = [s._count_pairs(ordered, t) for t in range(span + 2)]
        assert all(a <= b for a, b in zip(counts, counts[1:])), values

    # and the adjacency claim itself, which is the entire reason the candidate
    # form is linear-sized rather than quadratic. checked by brute force over all
    # pairings on small inputs: the best achievable maximum never beats what the
    # adjacent-only pairings achieve.
    def _perfect_matchings(items):
        if not items:
            yield []
            return
        first = items[0]
        for k in range(1, len(items)):
            partner = items[k]
            rest = items[1:k] + items[k + 1:]
            for tail in _perfect_matchings(rest):
                yield [(first, partner)] + tail

    def best_over_all_pairings(values, p):
        if p == 0:
            return 0
        ordered = sorted(values)
        n = len(ordered)
        best = None
        for chosen in itertools.combinations(range(n), 2 * p):
            for pairing in _perfect_matchings(list(chosen)):
                worst = max(ordered[b] - ordered[a] for a, b in pairing)
                if best is None or worst < best:
                    best = worst
        return best

    for values, p in cases:
        if len(values) > 7:
            continue
        assert s.minimizeMax(values, p) == best_over_all_pairings(values, p), (values, p)

    # the two searches share the predicate and nothing else - one walks the
    # integers, the other walks the gap list - so agreement is a test of the
    # adjacency argument rather than a restatement of it.
    for values, p in cases:
        assert s.minimizeMaxByCandidates(values, p) == s.minimizeMax(values, p), (
            values,
            p,
        )

    # attainment, which cost real work three days running and is free again here
    # for a different reason than 1898's. there the space was {0..n} and the
    # answer was an index into it. here the space is an interval of integers and
    # the answer is a member of a much smaller set inside it, and that it lands
    # there is the exchange argument being true.
    for values, p in cases:
        answer = s.minimizeMax(values, p)
        ordered = sorted(values)
        gaps = {ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1)}
        assert answer == 0 or answer in gaps, (values, p, answer, sorted(gaps))

    # the witness realises the answer exactly rather than merely respecting it.
    # this is attainment again, constructively: if the p greedy pairs all came in
    # strictly under the answer then the answer minus one would be feasible and
    # the search would have returned that instead.
    for values, p in cases:
        answer, pairs = s.minimizeMaxWitness(values, p)
        ordered = sorted(values)
        assert len(pairs) == p, (values, p, pairs)
        assert all(b == a + 1 for a, b in pairs), pairs
        flat = [i for pair in pairs for i in pair]
        assert flat == sorted(flat) and len(set(flat)) == len(flat), pairs
        assert all(ordered[b] - ordered[a] <= answer for a, b in pairs), pairs
        if p > 0:
            assert max(ordered[b] - ordered[a] for a, b in pairs) == answer, (
                values,
                p,
                pairs,
                answer,
            )

    # canonical in sorted-position space: equality against the leftmost greedy
    # computed independently, which is 1898's test.
    def leftmost_pairs(values, p, threshold):
        ordered = sorted(values)
        out = []
        i = 0
        while i + 1 < len(ordered) and len(out) < p:
            if ordered[i + 1] - ordered[i] <= threshold:
                out.append((i, i + 1))
                i += 2
            else:
                i += 1
        return out

    for values, p in cases:
        answer, pairs = s.minimizeMaxWitness(values, p)
        assert pairs == leftmost_pairs(values, p, answer), (values, p, pairs)

    # and not canonical in original-index space wherever there are ties, which is
    # the correction to yesterday. the multiset of *values* paired up is forced;
    # which physical elements carry those values is not, and the sort picked by an
    # accident of input order. so this half is a property check on the values.
    for values, p in cases:
        answer, pairs = s.minimizeMaxWitness(values, p)
        ordered = sorted(values)
        paired_values = sorted((ordered[a], ordered[b]) for a, b in pairs)
        shuffled = list(values)
        random.Random(len(values) * 31 + p).shuffle(shuffled)
        other_answer, other_pairs = s.minimizeMaxWitness(shuffled, p)
        other_ordered = sorted(shuffled)
        assert other_answer == answer, (values, shuffled, p)
        assert (
            sorted((other_ordered[a], other_ordered[b]) for a, b in other_pairs)
            == paired_values
        ), (values, shuffled, p)

    # p == 1 removes the search entirely, so the general path has to agree with a
    # min. this is also the only check that reliably lands on the bottom of the
    # range, since a random case reaches 0 only when it contains a duplicate.
    for values, _ in cases:
        if len(values) < 2:
            continue
        assert s.minimizeMax(values, 1) == s.minimizeMaxAllDistinctGaps(values, 1), values

    assert s.minimizeMaxAllDistinctGaps([1, 2, 3], 2) is None
    assert s.minimizeMaxAllDistinctGaps([1], 1) is None

    # every p from 0 up to the ceiling on the same array, so the boundary is
    # walked across rather than sampled. asking for more pairs can never lower the
    # answer, which is the monotonicity of the problem in p rather than of the
    # predicate in t - a different claim, and one nothing else here would catch.
    for values, _ in cases:
        previous = 0
        for p in range(len(values) // 2 + 1):
            answer = s.minimizeMax(values, p)
            assert answer >= previous, (values, p, answer, previous)
            assert s.minimizeMaxByCandidates(values, p) == answer, (values, p)
            previous = answer

    # random cases against the brute force, small enough that all pairings are
    # enumerable. the fixed cases are all hand-picked for a reason and hand-picked
    # cases stop finding things once they have been passed once.
    rng = random.Random(2616)
    for _ in range(300):
        n = rng.randint(1, 7)
        values = [rng.randint(0, 12) for _ in range(n)]
        p = rng.randint(0, n // 2)
        assert s.minimizeMax(values, p) == best_over_all_pairings(values, p), (values, p)
        assert s.minimizeMaxByCandidates(values, p) == s.minimizeMax(values, p), (
            values,
            p,
        )

    print("all good")
