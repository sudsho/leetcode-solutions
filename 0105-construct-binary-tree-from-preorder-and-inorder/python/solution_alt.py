# alt with explicit preorder index
from typing import List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]):
        idx = {v: i for i, v in enumerate(inorder)}
        self.pi = 0

        def helper(lo: int, hi: int):
            if lo > hi:
                return None
            v = preorder[self.pi]
            self.pi += 1
            node = TreeNode(v)
            i = idx[v]
            node.left = helper(lo, i - 1)
            node.right = helper(i + 1, hi)
            return node

        return helper(0, len(inorder) - 1)
