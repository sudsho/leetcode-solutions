class Solution:
    def minNumberOperations(self, target):
        # every problem in this family so far has run the map in one
        # direction: here is a pile of range updates, report the array they
        # accumulate to. this one hands over the accumulated array and asks
        # for the cheapest pile of range updates that produces it. so it is
        # the same map read backwards, and the reason that is even a
        # well-posed question is the thing worth taking away.
        #
        # the difference array is a bijection. an array of length n with an
        # implied 0 boundary determines its delta sequence and the delta
        # sequence determines it back, which is exactly why the accumulate
        # step loses nothing. all week that fact has been doing quiet work in
        # the background - it is the reason the two writes are allowed to
        # stand in for the whole range - and here it is the entire problem.
        #
        # so: an operation on [l, r] contributes +1 to d[l] and -1 to d[r+1],
        # and nothing else. the required d is fixed by the target. therefore
        #
        #     d[i] = (ops starting at i) - (ops ending at i-1)
        #
        # and since the second term is never negative, at least d[i] ops have
        # to start at i whenever d[i] > 0. every op starts somewhere exactly
        # once, so the total is at least the sum of the positive deltas. that
        # is a lower bound with no construction in it at all, which is what
        # makes it feel like a different kind of argument than the rest of the
        # week - nothing is being simulated, the counting is forced by the
        # structure of what an update can write.
        #
        # it is also achievable, and the third version below builds the ops to
        # show it rather than asserting it. the negative deltas never cost
        # anything because a close can always be paired with an already-open
        # start, so only the opens are ever paid for.
        #
        # target[0] is the first term because d[0] = target[0] - 0. the zero
        # boundary is not a special case, it is the same implied value that
        # made the closing write land past the end all week.
        total = target[0]
        for i in range(1, len(target)):
            rise = target[i] - target[i - 1]
            if rise > 0:
                total += rise
        return total

    def minNumberOperationsDivide(self, target):
        """Recursive: flatten to the minimum, then split there and recurse.

        The subarray covering a whole range can be applied `min - base` times
        before some position is finished, and every position holding that
        minimum is then done, so the range breaks into independent pieces
        between them. Cost is the flattening plus the pieces.

        This is the version I found first and it is worth keeping for a reason
        that is not speed. It is O(n^2) in the worst case here since the
        minimum is rescanned - a sparse table would make it O(n log n) - and
        the one-line answer above beats both. What it has instead is that it
        knows *why* each operation exists: each `min - base` is a real stack of
        subarrays over a real range. The linear version has already collapsed
        that into a count and cannot recover it.

        Fifth time this week the summary-versus-set distinction is what decides
        whether an alternate earns its place (2251, 2406, 699, 2158, now this).
        The difference is that in those it justified keeping a slower structure
        around for a hypothetical follow-up. Here the fast version is three
        lines and there is no structure at all, so the alternate is the only
        thing standing between the answer and an unexplained number.
        """
        def solve(lo, hi, base):
            if lo >= hi:
                return 0
            floor = min(target[lo:hi])
            cost = floor - base
            start = lo
            for i in range(lo, hi):
                if target[i] == floor:
                    cost += solve(start, i, floor)
                    start = i + 1
            cost += solve(start, hi, floor)
            return cost

        return solve(0, len(target), 0)

    def minNumberOperationsWithOps(self, target):
        """Build the actual operations, not just how many there are.

        Walks the same delta sequence the primary counts. A positive delta
        opens that many operations at i and pushes their start indices; a
        negative delta closes that many, and the one to close is whichever
        opened most recently, since the operations nest. Anything still open at
        the end runs to the last index.

        LIFO is correct rather than merely convenient. Two operations sharing a
        stretch are either nested or one starts after the other closes, and a
        later start closing before an earlier one would require them to cross,
        which no pair of intervals over a single delta sequence does. So the
        stack never has to choose.

        The returned list has exactly the length the primary reports, which is
        the achievability half of the bound written out instead of claimed.
        Kept separate from the count because the count is what the problem
        asks and this is O(answer) rather than O(n) - the target can be 10^5
        everywhere and then there are 10^5 operations to list.
        """
        ops = []
        open_starts = []
        previous = 0

        for i, value in enumerate(target):
            delta = value - previous
            for _ in range(delta):
                open_starts.append(i)
            for _ in range(-delta):
                ops.append((open_starts.pop(), i - 1))
            previous = value

        last = len(target) - 1
        while open_starts:
            ops.append((open_starts.pop(), last))

        return ops
