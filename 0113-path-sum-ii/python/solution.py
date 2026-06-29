from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None,
                 right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        # collect every root-to-leaf path whose values sum to targetSum.
        # dfs carrying the running path and remaining target; record a copy
        # only when we land on a leaf with the remainder exactly used up.
        paths: List[List[int]] = []
        path: List[int] = []

        def dfs(node: Optional[TreeNode], remaining: int) -> None:
            if node is None:
                return
            path.append(node.val)
            remaining -= node.val
            if node.left is None and node.right is None and remaining == 0:
                paths.append(path.copy())
            else:
                dfs(node.left, remaining)
                dfs(node.right, remaining)
            path.pop()  # backtrack before returning to the parent

        dfs(root, targetSum)
        return paths
