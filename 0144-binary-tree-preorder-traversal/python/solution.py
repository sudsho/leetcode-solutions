# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def preorderTraversal(self, root):
        """Iterative preorder (root, left, right) using an explicit stack.

        Push the right child before the left so the left is popped first and we
        visit nodes in root-left-right order. Avoids recursion depth limits on
        skewed trees.
        """
        out = []
        stack = [root] if root else []
        while stack:
            node = stack.pop()
            out.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return out
