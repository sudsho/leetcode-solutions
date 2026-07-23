class Solution:
    def invertTree(self, root):
        """Mirror the tree: swap every node's children top-down. Swap at the current
        node, then recurse into both sides (the order of the two recursions is free)."""
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
