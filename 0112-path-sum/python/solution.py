class Solution:
    def hasPathSum(self, root, targetSum):
        """Return True if some root-to-leaf path sums to targetSum.

        Walk down subtracting node values from the remaining target. A leaf
        contributes a valid path exactly when the remaining target hits its
        own value (i.e. remaining - val == 0).
        """
        if root is None:
            return False
        remaining = targetSum - root.val
        if root.left is None and root.right is None:
            return remaining == 0
        return (self.hasPathSum(root.left, remaining)
                or self.hasPathSum(root.right, remaining))
