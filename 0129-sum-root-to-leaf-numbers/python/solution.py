from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        # Each root-to-leaf path spells out a decimal number (root digit is most
        # significant). Carry the running prefix down: at every node the number so
        # far becomes prefix*10 + node.val. Add it into the total only at a leaf.
        def dfs(node: Optional[TreeNode], prefix: int) -> int:
            if node is None:
                return 0
            prefix = prefix * 10 + node.val
            if node.left is None and node.right is None:
                return prefix
            return dfs(node.left, prefix) + dfs(node.right, prefix)

        return dfs(root, 0)
