# stack variant, no recursion - walk postorder backwards using inorder to decide side
from typing import List


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]):
        if not postorder:
            return None
        root = TreeNode(postorder[-1])
        stack = [root]
        in_idx = len(inorder) - 1
        for i in range(len(postorder) - 2, -1, -1):
            val = postorder[i]
            node = stack[-1]
            if node.val != inorder[in_idx]:
                # still descending the right spine
                node.right = TreeNode(val)
                stack.append(node.right)
            else:
                # pop everything already matched in inorder, then attach left
                while stack and stack[-1].val == inorder[in_idx]:
                    node = stack.pop()
                    in_idx -= 1
                node.left = TreeNode(val)
                stack.append(node.left)
        return root
