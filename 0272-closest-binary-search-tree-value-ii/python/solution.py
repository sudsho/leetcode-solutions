from typing import List, Optional
from collections import deque

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def closestKValues(self, root: Optional[TreeNode], target: float, k: int) -> List[int]:
        out = deque()
        stack = []
        node = root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if len(out) < k:
                out.append(node.val)
            else:
                if abs(node.val - target) < abs(out[0] - target):
                    out.popleft()
                    out.append(node.val)
                else:
                    break
            node = node.right
        return list(out)
