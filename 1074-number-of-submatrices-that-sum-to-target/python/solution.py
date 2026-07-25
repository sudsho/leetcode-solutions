from collections import defaultdict


class Solution:
    def numSubmatrixSumTarget(self, matrix, target):
        rows, cols = len(matrix), len(matrix[0])

        # accumulate each row in place so row_prefix[r][c] is the sum of
        # columns 0..c in row r. that makes any horizontal strip O(1) later.
        row_prefix = [[0] * (cols + 1) for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                row_prefix[r][c + 1] = row_prefix[r][c] + matrix[r][c]

        total = 0
        # fix a pair of columns (c1, c2]; collapsing every row to its sum across
        # that band turns the 2d problem into 1d "subarrays summing to target",
        # which is exactly 560 - so run the same prefix-sum counter per band.
        for c1 in range(cols):
            for c2 in range(c1 + 1, cols + 1):
                seen = defaultdict(int)
                seen[0] = 1          # empty prefix, so a strip from row 0 counts
                running = 0
                for r in range(rows):
                    running += row_prefix[r][c2] - row_prefix[r][c1]
                    # every earlier prefix equal to running - target closes off
                    # a submatrix ending at row r within this column band.
                    total += seen[running - target]
                    seen[running] += 1
        return total
