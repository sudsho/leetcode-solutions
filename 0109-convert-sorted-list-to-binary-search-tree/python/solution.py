from typing import Optional

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None) -> None:
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val: int = 0, left: Optional["TreeNode"] = None, right: Optional["TreeNode"] = None) -> None:
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        size = 0
        node = head
        while node:
            size += 1
            node = node.next
        self._curr = head

        def build(n: int) -> Optional[TreeNode]:
            if n <= 0:
                return None
            left = build(n // 2)
            root = TreeNode(self._curr.val)
            self._curr = self._curr.next
            root.left = left
            root.right = build(n - n // 2 - 1)
            return root
        return build(size)
