from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        first = second = prev = None
        stack = []
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if prev and prev.val > node.val:
                if first is None:
                    first = prev
                second = node
            prev = node
            node = node.right
        if first and second:
            first.val, second.val = second.val, first.val
# follow up: revisit if profiling cares
