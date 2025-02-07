# revisited
class Solution:
    def diameterOfBinaryTree(self, root):
        self.best = 0

        def depth(node):
            if not node:
                return 0
            l = depth(node.left)
            r = depth(node.right)
            # candidate diameter through this node = l + r edges
            self.best = max(self.best, l + r)
            return 1 + max(l, r)

        depth(root)
        return self.best

# revisit: minor renames and one early exit added
