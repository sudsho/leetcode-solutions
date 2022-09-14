from typing import List, Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        def build(lo: int, hi: int) -> List[Optional[TreeNode]]:
            if lo > hi:
                return [None]
            trees: List[Optional[TreeNode]] = []
            for i in range(lo, hi + 1):
                for left in build(lo, i - 1):
                    for right in build(i + 1, hi):
                        trees.append(TreeNode(i, left, right))
            return trees
        return build(1, n) if n else []
