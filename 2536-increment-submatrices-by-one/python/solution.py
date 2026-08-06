class Solution:
    def rangeAddQueries(self, n, queries):
        # two days spent finding where the accumulator breaks, so today the
        # other direction. 699 broke it on composition, the update read the
        # state it wrote. 2158 broke it on attribution, the count was correct
        # and answered a different question. both of those were the technique
        # failing to reach the answer. this one is the question it has always
        # answered - how much landed on each cell - only asked over a grid
        # instead of a line, so it is a test of how far the same machinery
        # stretches rather than where it stops.
        #
        # it stretches by being run once per axis, and that is the whole
        # content of the 2d version. accumulate left to right along every row,
        # then top to bottom down every column, and the value sitting at
        # (r, c) is the sum of every diff entry weakly north-west of it. so
        # the writes have to be placed so that exactly the cells inside the
        # query rectangle see a net +1 and everything else sees zero. the 1d
        # answer was +1 at the open end and -1 past the close. the 2d answer
        # is the same two writes per axis multiplied out, which is the four
        # corners of inclusion-exclusion:
        #
        #     +1 at (r1, c1)          the rectangle opens
        #     -1 at (r1, c2+1)        cancel everything right of it
        #     -1 at (r2+1, c1)        cancel everything below it
        #     +1 at (r2+1, c2+1)      put back the quadrant cancelled twice
        #
        # the fourth write is the one that is easy to drop, and dropping it
        # does not fail on the rectangle itself, it fails on the cells south
        # -east of it, which no small hand-checked example tends to include.
        #
        # the closing writes are at c2+1 and r2+1 because the query bounds are
        # inclusive. seventh syntax for that decision in a week and a half and
        # the first time it has appeared twice in one problem, once per axis.
        # that is mildly reassuring rather than annoying: two independent
        # copies of the same call means it really is a property of the range
        # semantics and not of the dimension count.
        #
        # the pad is one row and one column, not two, since r2 and c2 are at
        # most n-1 and the closing write lands at n at worst.
        diff = [[0] * (n + 1) for _ in range(n + 1)]

        for r1, c1, r2, c2 in queries:
            diff[r1][c1] += 1
            diff[r1][c2 + 1] -= 1
            diff[r2 + 1][c1] -= 1
            diff[r2 + 1][c2 + 1] += 1

        # pass one: every row becomes its own 1d prefix sum. after this a cell
        # holds the net change for its own row only.
        for row in diff:
            for c in range(1, n + 1):
                row[c] += row[c - 1]

        # pass two: the same sweep down the columns. a cell now holds the sum
        # over the whole north-west quadrant, which is what the corner writes
        # were placed for.
        for r in range(1, n + 1):
            above, here = diff[r - 1], diff[r]
            for c in range(n + 1):
                here[c] += above[c]

        return [row[:n] for row in diff[:n]]

    def rangeAddQueriesSinglePass(self, n, queries):
        """Same writes, but accumulate in one pass with the 2d recurrence.

        grid[r][c] = diff[r][c] + grid[r-1][c] + grid[r][c-1] - grid[r-1][c-1]

        Worth writing out because it makes the symmetry explicit. The read side
        is four-corner inclusion-exclusion for exactly the reason the write side
        was: the two neighbouring quadrants overlap in the one to the north-west
        and it gets counted twice, so it is subtracted once. Same identity, same
        four terms, once when placing the deltas and once when consuming them.
        That is the same four-corner shape as the 2d fenwick tree in 308 and the
        band collapse in 1074, which I had been filing as a prefix-sum fact. It
        is not. It is a statement about rectangles, and the diff array and the
        prefix sum are the two directions of it.

        Not the primary version because the separable form says something the
        recurrence hides. Two independent 1d sweeps is a claim that the second
        axis adds nothing new, and that claim is the actual result here. The
        recurrence reads like a fact about 2d that has to be memorized on its
        own terms.
        """
        diff = [[0] * (n + 2) for _ in range(n + 2)]

        for r1, c1, r2, c2 in queries:
            diff[r1 + 1][c1 + 1] += 1
            diff[r1 + 1][c2 + 2] -= 1
            diff[r2 + 2][c1 + 1] -= 1
            diff[r2 + 2][c2 + 2] += 1

        # the extra pad row/column is here so r-1 and c-1 are always real
        # indices and the first row and column need no special case.
        for r in range(1, n + 1):
            for c in range(1, n + 1):
                diff[r][c] += diff[r - 1][c] + diff[r][c - 1] - diff[r - 1][c - 1]

        return [row[1:n + 1] for row in diff[1:n + 1]]

    def rangeAddQueriesRowwise(self, n, queries):
        """One 1d difference array per row, no second axis at all.

        For each query, walk the rows it spans and do the plain two-write
        update on each. O(q * n + n^2), against O(q + n^2) for the real
        version, so it is slower by exactly the row walk.

        Kept because it isolates what the second axis buys. This version is
        already correct and already uses the technique - it is 1109 applied
        r2 - r1 + 1 times - and the only thing wrong with it is that a query
        spanning every row costs n writes instead of 4. The 2d version does not
        compute anything this one cannot; it defers the row walk into the
        column sweep, which every cell has to pay for anyway. So the saving is
        not a better idea about rectangles, it is noticing that the vertical
        spreading is already being done for free by an accumulate that has to
        happen regardless.

        That also draws the line for when this version is the one to write. If
        the queries were few and n were large, the row walk is cheap and the
        n^2 sweep is the dominant cost, so paying it is the wrong trade. The
        break-even is q * n against n^2, meaning this loses only once q reaches
        n, which at the given bounds (n <= 500, q <= 10^4) it does.
        """
        rows = [[0] * (n + 1) for _ in range(n)]

        for r1, c1, r2, c2 in queries:
            for r in range(r1, r2 + 1):
                rows[r][c1] += 1
                rows[r][c2 + 1] -= 1

        result = []
        for row in rows:
            running = 0
            built = []
            for c in range(n):
                running += row[c]
                built.append(running)
            result.append(built)

        return result

    def rangeAddQueriesBrute(self, n, queries):
        """O(q * n^2): write into every cell of every rectangle.

        Times out at the real bounds - 10^4 queries over 500x500 is 2.5 * 10^9
        writes - but it is the statement of what the answer means, and the two
        faster versions are both just this one with the writes deferred rather
        than reorganized. Also the only version whose correctness needs no
        argument, which makes it the thing to diff against when the fourth
        corner write is wrong.
        """
        grid = [[0] * n for _ in range(n)]

        for r1, c1, r2, c2 in queries:
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    grid[r][c] += 1

        return grid
