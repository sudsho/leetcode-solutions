# Morris inorder, O(1) extra space
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        first = second = prev = None
        node = root
        while node:
            if node.left:
                pred = node.left
                while pred.right and pred.right is not node:
                    pred = pred.right
                if pred.right is None:
                    pred.right = node
                    node = node.left
                else:
                    pred.right = None
                    if prev and prev.val > node.val:
                        if first is None:
                            first = prev
                        second = node
                    prev = node
                    node = node.right
            else:
                if prev and prev.val > node.val:
                    if first is None:
                        first = prev
                    second = node
                prev = node
                node = node.right
        if first and second:
            first.val, second.val = second.val, first.val
