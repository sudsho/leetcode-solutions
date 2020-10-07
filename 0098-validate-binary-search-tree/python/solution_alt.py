# inorder traversal must be strictly increasing
class Solution:
    def isValidBST(self, root):
        prev = [float("-inf")]
        def go(node):
            if not node:
                return True
            if not go(node.left):
                return False
            if node.val <= prev[0]:
                return False
            prev[0] = node.val
            return go(node.right)
        return go(root)
