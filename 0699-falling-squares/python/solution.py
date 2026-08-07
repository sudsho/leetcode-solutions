from bisect import bisect_left


class _RangeAssignMaxTree:
    """Segment tree over gaps, supporting range assign and range max.

    Two operations, and the pairing is the whole reason this problem needs a
    tree at all:

        assign(l, r, v) : set every position in [l, r] to exactly v
        query(l, r)     : max over [l, r]

    Assign, not add. A landing square rests flat on whatever was underneath, so
    after it lands the entire span it covers has the same top height - the old
    heights beneath it are gone, not incremented. That is what makes the update
    non-invertible: there is no second write that undoes an assign the way a -1
    undoes a +1, so the difference array has nothing to work with here.

    Lazy assignment is stored as None-or-value rather than a separate flag,
    since 0 is a legitimate height and a truthiness test would silently skip
    pushing it down.
    """

    def __init__(self, size):
        self.size = size
        self.tree = [0] * (4 * size)
        self.lazy = [None] * (4 * size)

    def _apply(self, node, value):
        """Stamp `value` over this node's whole span.

        The tag *replaces* whatever tag is already here rather than combining
        with it. That is the one line where an assign tree differs from an add
        tree, where the tag would have to accumulate instead. Writing the
        composing version by habit still passes small tests, since the two
        disagree only when a second assign reaches a node before the first has
        been pushed down.
        """
        self.tree[node] = value
        self.lazy[node] = value

    def _push(self, node):
        """Hand this node's pending assignment to both children.

        Called before descending, so a child is never read or written while an
        ancestor still holds a tag that outranks it.
        """
        if self.lazy[node] is not None:
            self._apply(2 * node + 1, self.lazy[node])
            self._apply(2 * node + 2, self.lazy[node])
            self.lazy[node] = None

    def assign(self, left, right, value, node=0, lo=0, hi=None):
        hi = self.size - 1 if hi is None else hi
        if right < lo or hi < left:
            return
        if left <= lo and hi <= right:
            self._apply(node, value)
            return
        self._push(node)
        mid = (lo + hi) // 2
        self.assign(left, right, value, 2 * node + 1, lo, mid)
        self.assign(left, right, value, 2 * node + 2, mid + 1, hi)
        self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])

    def query(self, left, right, node=0, lo=0, hi=None):
        hi = self.size - 1 if hi is None else hi
        if right < lo or hi < left:
            return 0
        if left <= lo and hi <= right:
            return self.tree[node]
        self._push(node)
        mid = (lo + hi) // 2
        return max(self.query(left, right, 2 * node + 1, lo, mid),
                   self.query(left, right, 2 * node + 2, mid + 1, hi))


class Solution:
    def fallingSquares(self, positions):
        # this is the boundary of last week's technique, which is why it is
        # worth doing. every one of those problems had range updates that were
        # two writes and an accumulate, and that worked because the updates
        # composed: additively, commutatively, independently of the current
        # state. +1 over [a,b] then +1 over [c,d] is the same pile whichever
        # order they arrive in, so the pile collapses to one running number.
        #
        # here neither half holds. the value written by a square is
        # (max height already under it) + side, so the update READS the state
        # it is about to modify - and what it writes is an assignment, which
        # erases what was underneath instead of adding to it. two squares
        # dropped in the other order give a different skyline. an order-
        # dependent update cannot be summarized by an accumulator, so the
        # structure has to hold the actual heights: query then assign, which
        # is a segment tree with lazy propagation.
        #
        # note the interval is half-open. a square occupies [left, left+side)
        # and one starting exactly at left+side does not stack on it - they
        # only touch at a point. same inclusive-vs-half-open call as every
        # sweep problem this week, in yet another syntax: here it is which
        # compressed gap index the range stops at.
        # side >= 1, so every square contributes two distinct coordinates and
        # there is always at least one gap - no empty-tree case to guard.
        coords = sorted({c for left, side in positions
                         for c in (left, left + side)})
        tree = _RangeAssignMaxTree(len(coords) - 1)
        best = 0
        answer = []

        for left, side in positions:
            # gap i is the half-open span [coords[i], coords[i+1]). the square
            # covers gaps lo .. hi-1, so hi - 1 is the last one - that minus
            # one is the half-open boundary, and dropping it would stack
            # squares that merely touch.
            lo = bisect_left(coords, left)
            hi = bisect_left(coords, left + side)

            height = tree.query(lo, hi - 1) + side
            tree.assign(lo, hi - 1, height)

            best = max(best, height)
            answer.append(best)

        return answer

    def fallingSquaresBrute(self, positions):
        """O(n^2): keep the placed squares and scan them for each new drop.

        Accepted on the real constraints (n <= 1000) and the version worth
        writing first, because it states the recurrence with nothing in the way:
        a square's top is its side plus the tallest thing it lands on, and the
        only things it can land on are the earlier squares whose spans overlap
        its own.

        The overlap test is where the half-open boundary lives here. Strict
        comparisons on both sides, because squares that share only an endpoint
        sit side by side rather than one on the other - the same decision as the
        `hi - 1` in the tree version, relocated into a boolean.
        """
        placed = []  # (left, right, top) with right exclusive
        best = 0
        answer = []

        for left, side in positions:
            right = left + side
            base = 0
            for other_left, other_right, top in placed:
                if other_left < right and left < other_right:
                    base = max(base, top)

            height = base + side
            placed.append((left, right, height))
            best = max(best, height)
            answer.append(best)

        return answer

    def fallingSquaresIntervals(self, positions):
        """O(n^2) worst case, but keeps an explicit skyline of flat runs.

        Maintains a list of disjoint half-open segments (start, end, height)
        covering everything touched so far. A drop reads the max height over
        the segments it intersects, then splices itself in, trimming the
        partially-covered segments at each edge.

        Slower than the tree in theory and usually faster in practice at these
        sizes, but the reason to keep it is that it holds the skyline itself
        rather than a queryable summary of it. If the follow-up asked for the
        profile after all the drops, or the total area under it, this version
        already has the answer and the segment tree would have to be walked to
        reconstruct one. Same counts-collapse-but-sets-do-not distinction as
        2251 and 2406 - the summary is enough right up until it is not.
        """
        skyline = []  # sorted, disjoint (start, end, height), end exclusive
        best = 0
        answer = []

        for left, side in positions:
            right = left + side
            base = 0
            rebuilt = []

            for start, end, height in skyline:
                if end <= left or right <= start:
                    rebuilt.append((start, end, height))  # untouched
                    continue
                base = max(base, height)
                # keep whatever pokes out on either side; the middle is buried.
                if start < left:
                    rebuilt.append((start, left, height))
                if right < end:
                    rebuilt.append((right, end, height))

            rebuilt.append((left, right, base + side))
            skyline = sorted(rebuilt)

            best = max(best, base + side)
            answer.append(best)

        return answer
