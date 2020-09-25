class Solution:
    def isValidBST(self, root):
        def go(node, lo, hi):
            if not node:
                return True
            if node.val <= lo or node.val >= hi:
                return False
            return go(node.left, lo, node.val) and go(node.right, node.val, hi)

        return go(root, float("-inf"), float("inf"))
