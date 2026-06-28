class Solution:
    def buildTree(self, inorder, postorder):
        idx = {v: i for i, v in enumerate(inorder)}
        self.post = len(postorder) - 1

        def go(l, r):
            if l > r:
                return None
            root_val = postorder[self.post]
            self.post -= 1
            root = TreeNode(root_val)
            mid = idx[root_val]
            # postorder is left, right, root reversed -> build right before left
            root.right = go(mid + 1, r)
            root.left = go(l, mid - 1)
            return root

        return go(0, len(inorder) - 1)
