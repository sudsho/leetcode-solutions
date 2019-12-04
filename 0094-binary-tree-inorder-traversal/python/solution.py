class Solution:
    def inorderTraversal(self, root):
        out = []
        def walk(node):
            if not node:
                return
            walk(node.left)
            out.append(node.val)
            walk(node.right)
        walk(root)
        return out
