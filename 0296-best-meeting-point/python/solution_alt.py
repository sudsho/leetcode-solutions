# explicit-median variant: pick the median coordinate outright and sum the
# absolute deviations. same O(#homes) result, kept as the more literal reading
# of "everyone walks to the median row and the median column."
class Solution:
    def minTotalDistance(self, grid):
        rows, cols = [], []
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == 1:
                    rows.append(r)
                    cols.append(c)
        cols.sort()  # rows already ascending by construction
        mr = rows[len(rows) // 2]
        mc = cols[len(cols) // 2]
        return sum(abs(r - mr) for r in rows) + sum(abs(c - mc) for c in cols)
