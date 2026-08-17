class Solution:
    def maximumRemovals(self, s, p, removable):
        # seventh problem on the monotone-predicate-plus-bisect shape, and the
        # first one where the thing being searched isn't a quantity.
        #
        # the previous six all bisected a number that meant something on its
        # own - a budget, a distance, a load, a day, a gap width - and the
        # monotonicity came from the objective. more budget bought more, waiting
        # longer opened more flowers. the predicate was upward closed because
        # the resource was doing more work at a larger value.
        #
        # here k is an index into `removable` and nothing else. removable[3] is
        # not bigger than removable[1] in any sense; the array isn't sorted and
        # the positions have no order relation that matters. what k indexes is
        # the *set* removable[:k], and those sets are nested by construction:
        #
        #     {} subset removable[:1] subset removable[:2] subset ... subset removable
        #
        # p being a subsequence of s-minus-a-set is antitone in the set - taking
        # away more characters cannot create a match - so it's antitone along the
        # chain, so it's monotone in k. the whole monotonicity argument is that
        # prefixes nest. no exchange argument, no objective, nothing about what
        # the removals cost.
        #
        # that's the day. i'd been reading "binary search on the answer" as
        # requiring an ordered space of candidate answers with the predicate
        # ordered along it, and the ordered space kept being the answer's own
        # value because the problems kept being minimize-a-max. it needs a chain
        # and a predicate constant on each end of it. a chain of sets is a chain.
        n = len(removable)

        # low is feasible by assumption, not by argument. the problem promises p
        # is a subsequence of s, which is exactly "the predicate holds at k = 0".
        #
        # 1482 is where that stopped being free - the predicate could be false
        # everywhere and the bisect returned a plausible wrong number with no
        # symptom - and the fix there was a computed guard. the guard hasn't gone
        # away here. it moved into the problem statement. drop the promise and
        # this returns 0 for an input with no valid answer at all, in range and
        # silent, exactly the 1482 failure. the tests below assert the promise
        # rather than trusting it, since it's the only thing holding the bound up.
        low, high = 0, n

        # maximization, so the true half keeps mid and the true half is the one
        # that has to shrink: mid rounds up, low = mid. got this backwards once
        # by reaching for "yesterday was a min so today is a max", which is not
        # what decides it.
        while low < high:
            mid = (low + high + 1) // 2
            if self._still_subsequence(s, p, removable, mid):
                low = mid
            else:
                high = mid - 1

        return low

    def _still_subsequence(self, s, p, removable, k):
        """Is `p` still a subsequence of `s` after deleting `removable[:k]`?

        The deleted set is built fresh each call, which is the honest version of
        the predicate: it says "delete these, then check" and reads exactly like
        the problem. `O(n + k)` per call and the allocation dominates.

        The scan itself is the standard leftmost-match greedy - advance the `p`
        pointer whenever a surviving character matches. That greedy needs an
        exchange argument and it is easy to forget it has one, because the
        subsequence check is familiar enough to look like a definition. It isn't:
        the claim is that if any embedding of `p` exists then the leftmost one
        does, proved by pushing each matched position of an arbitrary embedding
        left to the earliest available slot, which never invalidates a later
        match since later positions only gain room.

        Three of the previous six had a predicate with a real greedy inside it
        and three had a formula. This has a greedy, and it's the first one whose
        exchange argument was already in my hands before the problem started.
        """
        removed = set(removable[:k])

        j = 0
        for i, ch in enumerate(s):
            if i in removed:
                continue
            if ch == p[j]:
                j += 1
                if j == len(p):
                    return True

        return False

    def maximumRemovalsByRank(self, s, p, removable):
        """Same search, with the chain made explicit instead of rebuilt each pass.

        `rank[i]` is the step at which position `i` is deleted, or `inf` if it
        never is. Then "position `i` survives `k` removals" is `rank[i] >= k`,
        a threshold on a label, and the set membership test disappears.

        This is the version that says what the search space is. The chain of
        nested prefixes is a single function from positions to the time they
        leave, and the bisect is scanning a threshold across that function's
        range. `removable` stops being an array being consumed and becomes a
        *labelling* of `s`, which is what it was the whole time - the order of
        the array is data about the positions, not an order on the answers.

        Strictly better than the primary and kept second anyway. The primary is
        the one that reads like the problem, and when the two disagree I want to
        find out by the transcription being right rather than by the clever one
        being right. Same reason 1482 kept the integer bisect as primary over the
        value-space version.
        """
        rank = [len(removable) + 1] * len(s)
        for step, index in enumerate(removable):
            rank[index] = step

        def survives(k):
            j = 0
            for i, ch in enumerate(s):
                if rank[i] < k:
                    continue
                if ch == p[j]:
                    j += 1
                    if j == len(p):
                        return True
            return False

        low, high = 0, len(removable)
        while low < high:
            mid = (low + high + 1) // 2
            if survives(mid):
                low = mid
            else:
                high = mid - 1

        return low

    def maximumRemovalsWitness(self, s, p, removable):
        """Return `(k, positions)` - the answer and where `p` lands in what's left.

        Thirteenth day of the summary-versus-set split and the first canonical
        witness in the run.

        The witness set has slack. `p = "ab"` in `s = "aab"` matches at either
        `a`, so there is more than one embedding and the answer cannot see which
        one, same as every day since 1552. But unlike 2528's unspent budget,
        2064's unused stores or 774's inert station, the slack here has a
        *direction*: the embeddings are ordered coordinatewise and there is a
        least one, so "leftmost" names a specific member of the set and the
        greedy already computes it.

        That's the distinction i'd been missing for twelve days by lumping every
        one of these under "the witness isn't canonical". The question is not
        whether the witness set has more than one element - it almost always
        does - but whether it has a distinguished element. A budget split three
        ways among tied cities has no canonical split because permuting the
        cities is a symmetry of the whole problem, so there is nothing to break
        the tie with. Positions in a string are not symmetric. Left is a real
        direction and the set is closed under moving that way.

        So this returns the leftmost embedding and the tests check equality with
        it rather than checking the property, which is the first time in the run
        that's been the right test to write.
        """
        k = self.maximumRemovals(s, p, removable)
        removed = set(removable[:k])

        positions = []
        j = 0
        for i, ch in enumerate(s):
            if i in removed:
                continue
            if ch == p[j]:
                positions.append(i)
                j += 1
                if j == len(p):
                    break

        # unreachable - k is feasible, so the same greedy that decided it also
        # completes here. raising rather than returning short: falling through
        # would mean the predicate and this scan disagree about the same k.
        if len(positions) != len(p):
            raise AssertionError("feasible k did not yield an embedding")

        return k, positions

    def maximumRemovalsExactMatch(self, s, p, removable):
        """Shortcut for `p == s`: the answer is 0.

        Every character is needed, so deleting any of them breaks the match and
        the first removal already fails. No search, no greedy, no predicate call
        beyond the one that isn't made.

        Same role as 1482's `k == 1` case - the input where the algorithm makes
        no decisions at all, so it's the cleanest thing to check the general path
        against. It also pins the `low = 0` end, which is the end the promise is
        holding up and the one the random cases never reach, since a random `p`
        drawn as a subsequence of a random `s` almost always has room to spare.

        Returns `None` when it does not apply, so it can't be used by accident on
        an input it says nothing about.
        """
        if s != p:
            return None

        return 0


if __name__ == "__main__":
    s = Solution()

    assert s.maximumRemovals("abcacb", "ab", [3, 1, 0]) == 2
    assert s.maximumRemovals("abcbddddd", "abcd", [3, 2, 1, 4, 5, 6]) == 1
    assert s.maximumRemovals("abcab", "abc", [0, 1, 2, 3, 4]) == 0
    assert s.maximumRemovals("qobftgcueho", "obue", [5, 3, 0, 6, 4, 9, 10, 7, 2, 8]) == 7
    assert s.maximumRemovals("a", "a", [0]) == 0

    cases = [
        ("abcacb", "ab", [3, 1, 0]),
        ("abcbddddd", "abcd", [3, 2, 1, 4, 5, 6]),
        ("abcab", "abc", [0, 1, 2, 3, 4]),
        ("qobftgcueho", "obue", [5, 3, 0, 6, 4, 9, 10, 7, 2, 8]),
        ("a", "a", [0]),
        ("aa", "a", [0]),
        ("aa", "a", [1, 0]),
        ("aaaa", "aa", [0, 3, 1, 2]),
        ("abab", "ab", [1, 2, 0, 3]),
        ("abcde", "ace", [1, 3]),
        ("abcde", "ace", [4, 0, 2]),
        ("xxxxx", "xx", [4, 3, 2]),
        ("leetcode", "let", [7, 6, 5, 4, 3, 2, 1, 0]),
        ("leetcode", "code", [0, 1, 2, 3]),
        ("mississippi", "misp", [10, 9, 8, 1, 2, 3]),
        ("abcdefghij", "adgj", [1, 2, 4, 5, 7, 8]),
    ]

    # the promise is what the low bound rests on, so it gets checked rather than
    # assumed. this is the 1482 guard, relocated into the problem statement -
    # without it the bisect returns 0 for an input with no answer and nothing
    # raises.
    def is_subsequence(s_, p_):
        it = iter(s_)
        return all(ch in it for ch in p_)

    for text, pattern, removable in cases:
        assert is_subsequence(text, pattern), (text, pattern)
        assert sorted(removable) == sorted(set(removable)), removable
        assert all(0 <= i < len(text) for i in removable), (text, removable)

    # the rank form shares the search but not the representation of the chain, so
    # agreement says the prefix-set and the threshold-on-a-label really are the
    # same object
    for text, pattern, removable in cases:
        assert s.maximumRemovalsByRank(text, pattern, removable) == s.maximumRemovals(
            text, pattern, removable
        ), (text, pattern, removable)

    # the predicate against its definition, directly. a predicate that's wrong but
    # still monotone hands back a confident wrong boundary with no symptom, which
    # is 1482's lesson and the reason this isn't checked through the search.
    def survives_brute(text, pattern, removable, k):
        kept = "".join(ch for i, ch in enumerate(text) if i not in set(removable[:k]))
        return is_subsequence(kept, pattern)

    for text, pattern, removable in cases:
        for k in range(len(removable) + 1):
            assert s._still_subsequence(text, pattern, removable, k) == survives_brute(
                text, pattern, removable, k
            ), (text, pattern, removable, k)

    # monotonicity along the chain, which every search here assumes and none of
    # them would notice failing. stated as "once false, false after" rather than
    # as a sorted-ness check, because that's the direction the bisect uses.
    for text, pattern, removable in cases:
        flags = [
            s._still_subsequence(text, pattern, removable, k)
            for k in range(len(removable) + 1)
        ]
        assert all(a >= b for a, b in zip(flags, flags[1:])), (text, pattern, removable)

    # and the nesting itself, which is the only reason the flags are monotone.
    # trivially true and written down because it's the entire argument - if the
    # search space were not a chain there would be nothing to bisect.
    for _, _, removable in cases:
        for k in range(len(removable)):
            assert set(removable[:k]) <= set(removable[: k + 1]), removable

    # linear scan from the top down, no bisect and no bounds, taking the first k
    # that works
    def brute(text, pattern, removable):
        for k in range(len(removable), -1, -1):
            if survives_brute(text, pattern, removable, k):
                return k
        return -1

    for text, pattern, removable in cases:
        assert s.maximumRemovals(text, pattern, removable) == brute(
            text, pattern, removable
        ), (text, pattern, removable)

    # the answer is always a member of the search space, and for the first time in
    # this run that's free rather than argued. 719 needed the boundary to be a
    # jump in the count, 1482 dodged it by bisecting the input values, 774 could
    # not have it at all because the answer set was attained but not enumerable.
    # here the space is {0..n} and the answer is an index into it by construction.
    for text, pattern, removable in cases:
        k = s.maximumRemovals(text, pattern, removable)
        assert isinstance(k, int) and 0 <= k <= len(removable), (text, k)

    # the witness is canonical, so it is checked against the leftmost embedding
    # computed independently rather than against the property. first day in the
    # run where that's the right test.
    def leftmost_embedding(text, pattern, removable, k):
        removed = set(removable[:k])
        out = []
        j = 0
        for i, ch in enumerate(text):
            if i in removed:
                continue
            if ch == pattern[j]:
                out.append(i)
                j += 1
                if j == len(pattern):
                    return out
        return None

    for text, pattern, removable in cases:
        k, positions = s.maximumRemovalsWitness(text, pattern, removable)
        assert k == s.maximumRemovals(text, pattern, removable), (text, pattern)
        assert positions == leftmost_embedding(text, pattern, removable, k), (
            text,
            pattern,
            removable,
        )
        # and it really is an embedding into what survives
        removed = set(removable[:k])
        assert positions == sorted(positions), positions
        assert all(i not in removed for i in positions), (positions, removed)
        assert "".join(text[i] for i in positions) == pattern, (text, pattern, positions)

    # p == s removes the search entirely, so the general path has to agree with a
    # constant. this is also the only check that lands on the low = 0 end.
    for text in ["a", "ab", "abc", "aaaa", "leetcode"]:
        removable = list(range(len(text)))
        assert s.maximumRemovals(text, text, removable) == s.maximumRemovalsExactMatch(
            text, text, removable
        ), text

    assert s.maximumRemovalsExactMatch("abc", "ab", [0]) is None

    # every prefix of `removable` used as its own instance, so the boundary is
    # walked across rather than sampled. truncating the array can only lower the
    # answer and can never raise it, which is the nesting claim again read from
    # the outside.
    for text, pattern, removable in cases:
        previous = 0
        for cut in range(len(removable) + 1):
            answer = s.maximumRemovals(text, pattern, removable[:cut])
            assert answer == brute(text, pattern, removable[:cut]), (text, cut)
            assert answer >= previous, (text, pattern, cut, answer, previous)
            assert answer <= cut, (text, cut, answer)
            previous = answer

    print("all good")
