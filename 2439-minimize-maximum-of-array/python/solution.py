import random
from collections import deque


class Solution:
    def minimizeArrayValue(self, nums):
        # fourteenth on the monotone-predicate-plus-bisect shape, and the first
        # one where the bisect does not happen.
        #
        # the last two days were an argument about what makes a predicate
        # invertible. on the 23rd i said the axis was expression versus black
        # box, then said that was too coarse because 2226's predicate is an
        # expression and still has to be searched, and replaced it with a count
        # of cheaply locatable breakpoints. then 2513 turned up with an O(1)
        # predicate and millions of breakpoints, which killed evaluation cost as
        # the axis but left the breakpoint count standing.
        #
        # the breakpoint count is wrong too, and this is the case that shows it.
        #
        # the predicate here is
        #
        #     fits(t)  <=>  for every i,  prefix[i] <= (i + 1) * t
        #
        # which is a **conjunction over an indexed family**, and every term is
        # linear in t. a conjunction of constraints each of which can be solved
        # for t is a max of the solved forms, so the whole search collapses:
        #
        #     answer = max over i of ceil(prefix[i] / (i + 1))
        #
        # there are n terms and therefore up to n breakpoints, which is more than
        # 1802 had and vastly more than the "few" the 23rd was reaching for, and
        # it makes no difference at all. what matters is not how many breakpoints
        # there are but whether the predicate **decomposes** into terms that can
        # each be inverted separately.
        #
        # that reads the previous three correctly for the first time:
        #
        #   1802  conjunction of 3 pieces, each a quadratic in t   -> inverts
        #   2226  a *sum* over the input, sum(c // t) >= k         -> terms are
        #         coupled by the summation, nothing to solve separately
        #   2513  conjunction of 3, but each term is floor-heavy   -> terms are
        #         separate and individually not invertible
        #   2439  conjunction of n, each term linear               -> inverts
        #
        # so there are two independent requirements - the predicate has to be a
        # conjunction rather than an aggregate, and the individual terms have to
        # be solvable - and the run has now produced a failure of each kind
        # separately. "how many breakpoints" was a proxy for the pair of them,
        # and it happened to track them on the four cases i had.
        prefix = 0
        best = 0

        for i, value in enumerate(nums):
            prefix += value
            # ceil(prefix / (i + 1)) without floats, since prefix reaches 1e14 at
            # the constraint ceiling and float64 has 53 bits of mantissa - not a
            # problem at 1e14, but the habit is worth more than the exception.
            candidate = -(-prefix // (i + 1))
            if candidate > best:
                best = candidate

        return best

    def _fits(self, nums, ceiling):
        """Can every entry be brought to `ceiling` or below?

        The whole problem is the reachability relation, and it is worth writing
        down before the predicate, because once it is written the predicate is a
        line of arithmetic.

        A move takes one unit from index `i` and puts it at `i - 1`. Units move
        **left and only left**, so for any prefix `[0..i]`, the total inside it
        can gain (from `i + 1`) and can never lose. That gives one direction of

            `b` is reachable from `a`  <=>  `b >= 0`, `sum(b) == sum(a)`, and
                                            `prefix_b[i] >= prefix_a[i]` for all i

        and the other direction is a greedy induction: given a legal target,
        repeatedly move the leftmost unit that is still to the right of where it
        needs to be. The `__main__` block checks this against a BFS over the full
        reachable set on small inputs rather than taking it on trust, because
        every claim below is a claim about this characterisation and not about
        the moves.

        Given it, feasibility of a ceiling `t` is a bound on prefixes. Each entry
        is at most `t`, so `prefix_b[i] <= (i + 1) * t`; combined with
        `prefix_b[i] >= prefix_a[i]` that forces

            prefix_a[i] <= (i + 1) * t        for every i

        and it is sufficient as well, since `prefix_b[i] = min((i + 1) * t, total)`
        satisfies every constraint at once - see `minimizeArrayValueWitness`.

        `O(n)`. Not used by the primary, which needs no predicate, and kept
        because the bisect is the thing thirteen problems have been about and the
        comparison is the point.
        """
        prefix = 0
        for i, value in enumerate(nums):
            prefix += value
            if prefix > (i + 1) * ceiling:
                return False
        return True

    def minimizeArrayValueBisect(self, nums):
        """The search this problem does not need, kept as an independent answer.

        Monotone in the usual direction - each constraint `prefix[i] <= (i+1)*t`
        is preserved by increasing `t`, so `{t : fits}` is a suffix and the
        minimisation keeps `mid` on the true side rounding down. Eleventh
        minimisation in fourteen.

        `O(n log(max prefix))`, against the primary's `O(n)`, and the gap is not
        the interesting part. The interesting part is that this function exists
        at all: it is the general method for a predicate you can only evaluate,
        and running it here is running a search over a set whose answer is
        already written down.
        """
        low, high = 0, max(nums) if nums else 0

        while low < high:
            mid = (low + high) // 2
            if self._fits(nums, mid):
                high = mid
            else:
                low = mid + 1

        return low

    def minimizeArrayValueWitness(self, nums):
        """Return `(answer, final)` - the value and an array achieving it.

        Twentieth day of the summary-versus-set split, and the first repeat.

        Four problems produced four different reasons for a canonical witness -
        meet-closure (1802), join-closure (2226), a total order on the candidate
        pool with no lattice anywhere (2513), and before those a leftmost
        convention (1898) - and i wrote on the 23rd that "canonical" had been a
        bucket rather than a property. This one is join-closure again, and it is
        the first time a mechanism has come back.

        The object it acts on is different, which is what makes the repeat worth
        something. 2226's join was on certificates. Here it is on **prefix
        vectors**: if `P` and `Q` are both feasible prefix vectors for ceiling
        `t`, so is their pointwise max, since

          - non-decreasing survives a pointwise max,
          - `>= prefix_a` survives it,
          - and each step still fits under `t`: if the max at `i` is `P[i]`, then
            `max(P,Q)[i] - max(P,Q)[i-1] <= P[i] - P[i-1] <= t`.

        So the feasible set has a greatest element, and it is the one built here:

            prefix_final[i] = min((i + 1) * t, total)

        - push every unit as far left as the ceiling allows. That is a witness
        chosen by a lattice fact rather than by a rule i made up, and it is worth
        being clear that the *optimum is not unique*: `[0, 3]` has answer 2 and
        both `[2, 1]` and `[1, 2]` attain it. The two are incomparable as arrays.
        They are not incomparable as prefix vectors - `[2, 3]` beats `[1, 3]` -
        and the ordering that makes the choice canonical is the one on prefixes,
        not the one on the thing the problem asks about. That is the part i had
        not seen in the four previous cases, because in all of them the witness
        and the object the order acted on were the same thing.

        `O(n)`.
        """
        answer = self.minimizeArrayValue(nums)
        total = sum(nums)

        final = []
        previous = 0
        for i in range(len(nums)):
            current = min((i + 1) * answer, total)
            final.append(current - previous)
            previous = current

        return answer, final

    def minimizeArrayValueNonDecreasing(self, nums):
        """Shortcut for a non-decreasing input: the answer is the whole average.

        If `nums` is non-decreasing then `prefix[i] / (i + 1)` is a running mean
        of a non-decreasing sequence and is therefore itself non-decreasing, so
        the max over `i` is attained at the last index and the answer is
        `ceil(total / n)` with no scan of the intermediate prefixes at all.

        Same role as 2513's equal-divisors path and 2141's `n == 1`: an input
        where the general method makes no decisions, computed by a route that
        shares no arithmetic with it, so agreement is a cross-check rather than a
        restatement.

        The subtlety is that the ceiling does not distribute over the max - it is
        the *means* that are ordered, not their ceilings, but ceil is monotone so
        the order survives it. That is the whole proof and it is the kind of step
        that is easy to skip and wrong to skip: `max(ceil(x_i)) == ceil(max(x_i))`
        needs monotone ceil, not linear ceil.

        Returns `None` when it does not apply.
        """
        if any(a > b for a, b in zip(nums, nums[1:])):
            return None

        return -(-sum(nums) // len(nums))


def reachable(source, target):
    """Is `target` reachable from `source` under the move, by the characterisation?

    Kept outside the class because it is the statement being tested rather than
    part of any answer.
    """
    if len(source) != len(target) or any(v < 0 for v in target):
        return False

    ps = qs = 0
    for a, b in zip(source, target):
        ps += a
        qs += b
        if qs < ps:
            return False

    return ps == qs


def reachable_bfs(source):
    """Every array reachable from `source`, by actually making the moves.

    Exponential and only usable on tiny inputs, which is the point - it is the
    only thing here that does not go through the prefix characterisation.
    """
    start = tuple(source)
    seen = {start}
    queue = deque([start])

    while queue:
        state = queue.popleft()
        for i in range(1, len(state)):
            if state[i] > 0:
                nxt = list(state)
                nxt[i] -= 1
                nxt[i - 1] += 1
                nxt = tuple(nxt)
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)

    return seen


if __name__ == "__main__":
    s = Solution()

    assert s.minimizeArrayValue([3, 7, 1, 6]) == 5
    assert s.minimizeArrayValue([10, 1]) == 10
    assert s.minimizeArrayValue([0, 3]) == 2
    assert s.minimizeArrayValue([5]) == 5
    assert s.minimizeArrayValue([0, 0, 0]) == 0

    cases = [
        [3, 7, 1, 6],
        [10, 1],
        [0, 3],
        [5],
        [0, 0, 0],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [0, 0, 0, 12],
        [12, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1],
        [2, 2, 2, 2],
        [0, 1, 0, 1, 100],
        [10 ** 9, 0, 0],
        [0, 0, 10 ** 9],
        [7, 0, 7, 0, 7, 0],
    ]

    # the characterisation the whole file rests on, against a BFS over the actual
    # moves. this is the only check here that touches the moves at all - every
    # other claim below is about prefix vectors, so if this is wrong then nothing
    # else means anything and all of it would still pass.
    for source in ([0, 3], [1, 2, 1], [2, 0, 2], [3, 1, 0], [0, 0, 4], [1, 1, 1, 1]):
        by_moves = reachable_bfs(source)
        total = sum(source)
        span = total + 1

        # enumerate every non-negative array with the right total and compare the
        # two memberships, rather than only checking the ones the BFS found - the
        # characterisation has to be wrong in neither direction.
        def compositions(n, k):
            if k == 1:
                yield (n,)
                return
            for first in range(n + 1):
                for rest in compositions(n - first, k - 1):
                    yield (first,) + rest

        for candidate in compositions(total, len(source)):
            assert reachable(source, list(candidate)) == (candidate in by_moves), (
                source,
                candidate,
            )

        assert span >= 1

    # the answer against the reachable set, computed by BFS with no formula in it.
    for source in ([0, 3], [1, 2, 1], [2, 0, 2], [3, 1, 0], [0, 0, 4], [1, 1, 1, 1],
                   [0, 5, 1], [2, 3, 0, 1]):
        best = min(max(state) for state in reachable_bfs(source))
        assert s.minimizeArrayValue(source) == best, (source, best)

    # the bisect agrees with the closed form. it is a genuinely different
    # computation - it evaluates the predicate at points it chooses and never
    # solves anything - so agreement is a cross-check on the inversion, which is
    # the one step today that could be silently wrong.
    for nums in cases:
        assert s.minimizeArrayValueBisect(nums) == s.minimizeArrayValue(nums), nums

    # necessity: one below the answer fails the predicate. sufficiency: the answer
    # passes it. together these pin the boundary without a search and without the
    # BFS, and neither half is brute force.
    for nums in cases:
        answer = s.minimizeArrayValue(nums)
        assert s._fits(nums, answer), nums
        if answer > 0:
            assert not s._fits(nums, answer - 1), nums

    # the witness. this is the sufficiency half done by construction: the greatest
    # feasible prefix vector, turned back into an array, has to be reachable and
    # has to attain the answer. a theorem about the lattice is not a theorem about
    # the arithmetic that walks it.
    for nums in cases:
        answer, final = s.minimizeArrayValueWitness(nums)
        assert len(final) == len(nums), nums
        assert sum(final) == sum(nums), nums
        assert all(v >= 0 for v in final), (nums, final)
        assert max(final) == answer, (nums, final, answer)
        assert reachable(nums, final), (nums, final)

    # and the witness really is the *greatest* prefix vector and not merely a
    # feasible one, checked against every optimal array the BFS can find. this is
    # the claim that the repeat of join-closure is a repeat and not a story told
    # after the fact.
    for source in ([0, 3], [1, 2, 1], [2, 0, 2], [0, 5, 1], [2, 3, 0, 1], [0, 0, 4]):
        answer, final = s.minimizeArrayValueWitness(source)

        def prefixes(seq):
            out, running = [], 0
            for v in seq:
                running += v
                out.append(running)
            return out

        mine = prefixes(final)
        optimal = [st for st in reachable_bfs(source) if max(st) == answer]
        assert optimal, source
        for state in optimal:
            assert all(a >= b for a, b in zip(mine, prefixes(state))), (source, state)

        # and the optimum is genuinely not unique in general, so the lattice is
        # doing real work rather than picking the only candidate there was
        assert len(optimal) >= 1

    ties = [st for st in reachable_bfs([0, 3]) if max(st) == 2]
    assert len(ties) == 2, ties

    # the non-decreasing shortcut, on the inputs where it applies. it shares no
    # arithmetic with the primary - one ceiling of the whole total against a max
    # over n of them - so its agreement says the max is being taken over the right
    # family and not just evaluated correctly.
    for nums in cases:
        shortcut = s.minimizeArrayValueNonDecreasing(nums)
        if shortcut is not None:
            assert shortcut == s.minimizeArrayValue(nums), nums

    assert s.minimizeArrayValueNonDecreasing([5, 4]) is None

    # monotonicity in the direction a bisect would need, checked even though
    # nothing here bisects except the cross-check. a predicate that is wrong but
    # monotone gives a confident wrong boundary and nothing downstream notices.
    for nums in cases:
        top = min(max(nums), 300)
        flags = [s._fits(nums, t) for t in range(0, top + 1)]
        assert all(a <= b for a, b in zip(flags, flags[1:])), nums

    # random cases against the BFS, which is the only route that never mentions a
    # prefix. small totals on purpose, since the reachable set is a composition
    # count and blows up immediately.
    rng = random.Random(2439)
    for _ in range(200):
        n = rng.randint(1, 5)
        nums = [rng.randint(0, 3) for _ in range(n)]

        states = reachable_bfs(nums)
        best = min(max(state) for state in states)
        assert s.minimizeArrayValue(nums) == best, (nums, best)

        answer, final = s.minimizeArrayValueWitness(nums)
        assert answer == best and max(final) == best, (nums, final)
        assert tuple(final) in states, (nums, final)

    # bounds, tenth day, and there is no range.
    #
    # nine days of a bottom end and a top end, three kinds of bottom and two of
    # top, and today the section has nothing in it, because there is no interval
    # to bracket. the bisect kept as a cross-check needs one and gets
    # `[0, max(nums)]` - zero is feasible exactly when every entry is zero, and
    # `max(nums)` is feasible because doing nothing attains it - but that is a
    # range for the check rather than for the answer.
    #
    # worth saying plainly: for nine days "what are the bounds" felt like a
    # question about the problem, and it is a question about the method. no
    # search, no bounds.
    for nums in cases:
        assert s._fits(nums, max(nums)), nums
        assert s.minimizeArrayValue(nums) <= max(nums), nums

    # at the constraint ceiling, since the whole note today is that the number of
    # breakpoints does not matter and every case above has almost none. 1e5
    # entries at 1e9 puts the prefix at 1e14, past 2**32 and well inside float64's
    # exact-integer range, which is why the ceiling above is written with `-(-a//b)`
    # rather than with `math.ceil`.
    big = [10 ** 9] * (10 ** 5)
    assert s.minimizeArrayValue(big) == 10 ** 9
    assert s.minimizeArrayValue([0] * (10 ** 5 - 1) + [10 ** 9]) == 10000
    assert s.minimizeArrayValue([10 ** 9] + [0] * (10 ** 5 - 1)) == 10 ** 9

    spike = [0] * (10 ** 5)
    spike[1] = 10 ** 9
    assert s.minimizeArrayValue(spike) == 5 * 10 ** 8

    print("all good")
