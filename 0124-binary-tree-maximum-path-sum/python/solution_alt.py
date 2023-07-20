# 2023 nit (133)
# explicit nonlocal best
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root) -> int:
        best = float("-inf")

        def gain(node) -> int:
            nonlocal best
            if not node:
                return 0
            l = max(gain(node.left), 0)
            r = max(gain(node.right), 0)
            best = max(best, node.val + l + r)
            return node.val + max(l, r)

        gain(root)
        return best
