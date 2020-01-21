class Solution:
    def buildTree(self, preorder, inorder):
        idx = {v: i for i, v in enumerate(inorder)}
        self.pre = 0

        def go(l, r):
            if l > r:
                return None
            root_val = preorder[self.pre]
            self.pre += 1
            root = TreeNode(root_val)
            mid = idx[root_val]
            root.left = go(l, mid - 1)
            root.right = go(mid + 1, r)
            return root

        return go(0, len(inorder) - 1)
