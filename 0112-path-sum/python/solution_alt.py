class Solution:
    def hasPathSum(self, root, targetSum):
        """Iterative variant - explicit stack instead of recursion.

        Each stack entry carries a node together with the running sum down to
        and including that node. When we pop a leaf whose running sum equals
        targetSum we have found a valid path.
        """
        if root is None:
            return False
        stack = [(root, root.val)]
        while stack:
            node, total = stack.pop()
            if node.left is None and node.right is None and total == targetSum:
                return True
            if node.left:
                stack.append((node.left, total + node.left.val))
            if node.right:
                stack.append((node.right, total + node.right.val))
        return False
