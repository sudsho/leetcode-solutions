# explicit two-stack version
from typing import List, Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        out: List[int] = []
        stack = []
        last = None
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            peek = stack[-1]
            if peek.right and peek.right is not last:
                node = peek.right
            else:
                out.append(peek.val)
                last = stack.pop()
        return out
