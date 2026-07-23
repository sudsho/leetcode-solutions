# iterative variant - walk down to the empty child and attach, no recursion stack

class Solution:
    def insertIntoBST(self, root, val):
        node = TreeNode(val)
        if root is None:
            return node
        cur = root
        while True:
            if val < cur.val:
                if cur.left is None:
                    cur.left = node
                    return root
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    return root
                cur = cur.right
