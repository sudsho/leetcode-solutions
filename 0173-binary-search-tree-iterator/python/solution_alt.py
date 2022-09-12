# precompute the inorder list - simple but uses O(N) space
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    def __init__(self, root: Optional[TreeNode]) -> None:
        self.values: List[int] = []
        self._inorder(root)
        self.idx = 0

    def _inorder(self, node: Optional[TreeNode]) -> None:
        if node is None:
            return
        self._inorder(node.left)
        self.values.append(node.val)
        self._inorder(node.right)

    def next(self) -> int:
        v = self.values[self.idx]
        self.idx += 1
        return v

    def hasNext(self) -> bool:
        return self.idx < len(self.values)
