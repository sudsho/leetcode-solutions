from heapq import heappush, heappop


class Solution:
    def minGroups(self, intervals):
        # the grouping is a red herring. two intervals must be split iff they
        # overlap, so the answer is the largest set of intervals that are all
        # live at once - and for intervals, pairwise overlap implies a common
        # point (helly in one dimension), so that set is pinned to a single
        # coordinate. so: max number of intervals covering any one point.
        #
        # which is the diff array again, with the fifth different reading of
        # the accumulator. 1109 wanted its final value, 2848 wanted whether it
        # was positive, 1094 wanted it checked against a bound every step,
        # 2381 wanted it mod 26. this one wants its MAXIMUM over the sweep,
        # which is the first reading that needs the accumulation kept rather
        # than consumed - the running total has to be watched the whole way,
        # like 1094, but reported at the end, like 1109.
        limit = max(r for _, r in intervals)
        diff = [0] * (limit + 2)

        for left, right in intervals:
            # inclusive range, so the cancel goes one past the last covered
            # point. sizing limit + 2 is what makes that legal for the widest
            # interval instead of needing a bounds guard.
            diff[left] += 1
            diff[right + 1] -= 1

        best = 0
        running = 0
        for delta in diff:
            running += delta
            best = max(best, running)

        return best

    def minGroupsHeap(self, intervals):
        """Sort by start, keep the group end-times in a min-heap.

        This is the version that actually constructs an assignment rather than
        just counting one, and it makes the greedy visible: when an interval
        arrives, reusing any group whose last interval has already ended is
        free, so only open a new group when none has. The heap only needs the
        earliest-ending group, because if that one does not fit no other does.

        Same O(n log n) as the array version is O(n + C), and which wins is the
        usual coordinate-space question - here C = 10^6 against n = 10^5, so
        the array allocates ten slots per interval to save the sort.
        """
        intervals = sorted(intervals)
        group_ends = []  # min-heap of the last end time in each open group

        for left, right in intervals:
            # a group is reusable when its last interval ended strictly before
            # this one starts. ends are inclusive, so touching at a point is
            # still an overlap and the comparison has to be < left, not <= -
            # same inclusive-vs-half-open call as the closing write above.
            if group_ends and group_ends[0] < left:
                heappop(group_ends)
            heappush(group_ends, right)

        return len(group_ends)

    def minGroupsTwoPointer(self, intervals):
        """Sort the two endpoint lists independently and merge-walk them.

        Drops the heap entirely: the sweep only ever needs to know how many
        intervals have opened minus how many have closed, and neither count
        cares which interval it belonged to. So the pairing between a start and
        its own end can be thrown away, which is exactly what sorting the two
        columns separately does.

        This is the same collapse as 2251 seen from the other side - there the
        two sorted endpoint lists got binary searched at m query points, here
        they get walked once because every point is a query point.
        """
        starts = sorted(left for left, _ in intervals)
        ends = sorted(right for _, right in intervals)

        best = 0
        live = 0
        j = 0
        for start in starts:
            # retire everything that finished before this interval opens.
            # ends[j] < start, strict again for the inclusive-endpoint reason.
            while ends[j] < start:
                live -= 1
                j += 1
            live += 1
            best = max(best, live)

        return best

    def minGroupsNaive(self, intervals):
        """O(n^2) pairwise overlap count, for reference on small inputs.

        Builds the conflict graph and returns its largest clique, which is only
        tractable because interval graphs are perfect - the clique is the point
        with the most coverage, which is what the sweep finds in O(n log n).
        """
        best = 0
        for left, right in intervals:
            for point in (left, right):
                covering = sum(1 for a, b in intervals if a <= point <= b)
                best = max(best, covering)
        return best
