class Solution:
    def maxDepth(self, root):
        """Depth of the deepest leaf. Recurse into both subtrees and take the
        larger depth plus one for the current node; an empty tree has depth 0."""
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
