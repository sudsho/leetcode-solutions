# recursive variant filling levels
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        out: List[List[int]] = []

        def walk(node, depth: int) -> None:
            if not node:
                return
            if depth == len(out):
                out.append([])
            out[depth].append(node.val)
            walk(node.left, depth + 1)
            walk(node.right, depth + 1)

        walk(root, 0)
        return out
