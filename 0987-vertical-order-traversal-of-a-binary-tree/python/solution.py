from collections import defaultdict


class Solution:
    def verticalTraversal(self, root):
        """Group nodes by column (root at col 0, left = col-1, right = col+1).
        Within a column, order top to bottom by row; break same-row-same-column ties
        by node value. Collect (row, val) per column, then sort each column's list."""
        cols = defaultdict(list)      # col -> list of (row, val)
        stack = [(root, 0, 0)]        # (node, row, col)
        while stack:
            node, row, col = stack.pop()
            if node is None:
                continue
            cols[col].append((row, node.val))
            stack.append((node.left, row + 1, col - 1))
            stack.append((node.right, row + 1, col + 1))

        out = []
        for col in sorted(cols):
            # sort by (row, val): row is primary, value breaks ties within a cell
            out.append([val for _, val in sorted(cols[col])])
        return out
