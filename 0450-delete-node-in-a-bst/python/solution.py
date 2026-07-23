class Solution:
    def deleteNode(self, root, key):
        """Standard BST delete. Recurse to locate the node. Removing it splits into
        three cases: no children (drop it), one child (splice it out), two children
        (copy in the in-order successor - the smallest key in the right subtree - then
        delete that successor, which by construction has at most one child)."""
        if root is None:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            # found the target
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            # two children: pull up the in-order successor
            succ = root.right
            while succ.left:
                succ = succ.left
            root.val = succ.val
            root.right = self.deleteNode(root.right, succ.val)
        return root
