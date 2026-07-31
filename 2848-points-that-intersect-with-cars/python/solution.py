class Solution:
    def numberOfPoints(self, nums):
        # same difference array as 1109, but the question is about COVERAGE
        # rather than totals - how many integer points sit under at least one
        # car. so the accumulated value stops being an answer in itself and
        # becomes a predicate: running > 0 means "something covers me here".
        #
        # the constraint end <= 100 is the reason this is easy. the coordinate
        # space is tiny and fixed, so the array can just span it and there is
        # no need to compress anything.
        MAX_POINT = 100
        diff = [0] * (MAX_POINT + 2)  # +2: index 101 absorbs a car ending at 100

        for start, end in nums:
            # +1 where the car starts covering, -1 at end + 1 because the range
            # is inclusive and end itself is still under the car. exactly the
            # off-by-one from 1109, except the points are already 1-indexed on
            # both sides so there is no -1 on the opening write this time.
            diff[start] += 1
            diff[end + 1] -= 1

        # accumulate, and count the positions where at least one car is open.
        # overlaps take care of themselves: two cars over the same point push
        # running to 2, which is still just "covered" once.
        covered = 0
        running = 0
        for point in range(1, MAX_POINT + 1):
            running += diff[point]
            if running > 0:
                covered += 1

        return covered

    def numberOfPointsMerge(self, nums):
        """Alt: sort and merge the intervals, then sum their lengths.

        This is the version that survives the constraint being lifted - it
        depends on the number of cars, not on how wide the coordinate space is,
        so it is what you reach for when the endpoints go up to 10^9 and an
        array over the range stops being an option.
        """
        covered = 0
        current_start, current_end = None, None

        for start, end in sorted(nums):
            if current_end is None or start > current_end + 1:
                # disjoint from the run being built (and not merely adjacent -
                # [1,3] and [4,5] touch with no integer gap, so they still
                # merge). close out the previous run and open a new one.
                if current_end is not None:
                    covered += current_end - current_start + 1
                current_start, current_end = start, end
            else:
                # overlapping or adjacent, so extend. max() matters because a
                # sorted-by-start order says nothing about the ends - [1, 10]
                # then [2, 3] would otherwise shrink the run.
                current_end = max(current_end, end)

        if current_end is not None:
            covered += current_end - current_start + 1

        return covered
