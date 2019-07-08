class Solution:
    def isSymmetric(self, root):
        if not root:
            return True

        def mirror(a, b):
            if not a and not b:
                return True
            if not a or not b:
                return False
            if a.val != b.val:
                return False
            # cross compare
            return mirror(a.left, b.right) and mirror(a.right, b.left)

        return mirror(root.left, root.right)
