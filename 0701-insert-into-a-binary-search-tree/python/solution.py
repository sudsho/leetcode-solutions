# Definition for a binary tree node (provided by the judge):
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val, self.left, self.right = val, left, right

class Solution:
    def insertIntoBST(self, root, val):
        """Recursive insert. Follow the BST invariant down to the empty slot where
        val belongs and hang a new leaf there. Any valid leaf position is accepted."""
        if root is None:
            return TreeNode(val)
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)
        return root
