class Solution:
    def convertBST(self, root):
        """Replace each key with itself plus the sum of all greater keys. A reverse
        in-order traversal (right, node, left) visits keys in descending order, so a
        running accumulator holds the sum of everything already seen (all greater)."""
        acc = 0

        def visit(node):
            nonlocal acc
            if not node:
                return
            visit(node.right)     # larger keys first
            acc += node.val
            node.val = acc
            visit(node.left)      # then smaller keys

        visit(root)
        return root
