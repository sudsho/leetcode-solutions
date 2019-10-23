class Solution:
    def invertTree(self, root):
        if not root:
            return None
        # swap children, then recurse
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root

# optim: pass small inputs straight through above
